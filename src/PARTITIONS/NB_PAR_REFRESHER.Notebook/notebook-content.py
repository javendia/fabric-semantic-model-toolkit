# Fabric notebook source

# METADATA ********************

# META {
# META   "kernel_info": {
# META     "name": "jupyter",
# META     "jupyter_kernel_name": "python3.11"
# META   },
# META   "dependencies": {}
# META }

# PARAMETERS CELL ********************

workspace_id: str = ""
dataset_id: str = ""
tables_to_refresh: str = ""
partitions_to_refresh: str = ""
commit_mode: str = ""
max_parallelism: int = 4

# METADATA ********************

# META {
# META   "language": "python",
# META   "language_group": "jupyter_python"
# META }

# CELL ********************

import pandas as pd
import logging
import sys
from typing import List, Optional
from io import StringIO
from fabtoolkit.utils import is_valid_text
from fabtoolkit.log import ConsoleLogFormatter
from fabtoolkit.dataset import Dataset

# METADATA ********************

# META {
# META   "language": "python",
# META   "language_group": "jupyter_python"
# META }

# CELL ********************

# Constants
DEFAULT_LOG_LEVEL = logging.DEBUG

# METADATA ********************

# META {
# META   "language": "python",
# META   "language_group": "jupyter_python"
# META }

# CELL ********************

logger = logging.getLogger("refresher")
logger.setLevel(DEFAULT_LOG_LEVEL)
logger.propagate = False

if not logger.handlers:
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setFormatter(ConsoleLogFormatter())
    console_handler.setLevel(DEFAULT_LOG_LEVEL)
    logger.addHandler(console_handler)

# METADATA ********************

# META {
# META   "language": "python",
# META   "language_group": "jupyter_python"
# META }

# CELL ********************

def get_tables(dataset: Dataset, tables_to_refresh: Optional[str]) -> pd.DataFrame:
    """
    Gets the list of tables to refresh. 
    If tables parameter is provided, parse it into a list and get related tables. 
    If not provided, retrieve all tables from the dataset.

    Args:
        dataset (Dataset): Dataset object.
        tables_to_refresh (Optional[str]): Comma-separated string of table names to refresh.

    Returns:
        pd.DataFrame: DataFrame containing table names to refresh.

    Raises:
        ValueError: If no tables to refresh are found or invalid table names are provided.
    """
    
    available_tables: List[str] = dataset.tables["table_name"].unique().tolist()
    
    if is_valid_text(tables_to_refresh):
        table_list: List[str] = [t.strip() for t in tables_to_refresh.split(',') if t.strip()]
        logger.info(f"Tables to refresh provided: {table_list}")
        
        # Check if the provided tables exist in the dataset
        
        invalid_tables: List[str] = list(set(table_list) - set(available_tables))
        valid_tables: List[str] = []
        if invalid_tables:
            valid_tables =  list(set(table_list) - set(invalid_tables))
            if not valid_tables:
                raise ValueError("All provided tables to refresh are invalid.")
            logger.warning(f"Invalid table names provided: {invalid_tables}")
        else:
            valid_tables = table_list
        
        # Get related tables for selected tables, excluding invalid ones
        tables: pd.DataFrame = dataset.get_related_tables(list(set(table_list) - set(invalid_tables)))
        logger.info(f"Tables to refresh: {tables['table_name'].tolist()}")
        return tables
    else:
        logger.info("No tables to refresh provided. Retrieving all tables...")
        return pd.DataFrame({"table_name": available_tables})

# METADATA ********************

# META {
# META   "language": "python",
# META   "language_group": "jupyter_python"
# META }

# CELL ********************

def get_partitions(dataset: Dataset, tables: pd.DataFrame, partitions_to_refresh: str) -> pd.DataFrame:
    """
    Gets the list of partitions to refresh.
    If partitions parameter is provided, parse it, validate, and filter the partitions to refresh.
    If not provided, retrieve all partitions from the dataset.

    Args:
        dataset (Dataset): Dataset object.
        tables (pd.DataFrame): DataFrame of tables to refresh.
        partitions_to_refresh (str): JSON string specifying tables and their partitions to refresh.
    
    Returns:
        pd.DataFrame: Partitions to refresh.
    
    Raises:
        ValueError: If invalid partitions are specified.
    """

    # Get partitions for each table to refresh
    available_partitions: pd.DataFrame = tables.merge(
        dataset.partitions,
        on=["table_name"],
        how="inner"
    )[["table_name", "partition_name"]]

    if not is_valid_text(partitions_to_refresh):
        logger.info("No explicit partitions to refresh. Refreshing all partitions...")
        return available_partitions
    else:
        # Parse and explode selected partitions
        selected_partitions: pd.DataFrame = (
            pd.read_json(StringIO(partitions_to_refresh))
            .assign(partition=lambda x: x["selected_partitions"].str.split(','))
            .explode("partition", ignore_index=True)
            .assign(partition=lambda x: x["partition"].str.strip())
        )

        # If any of the tables with selected partitions are not available
        selected_partitions["is_valid_table"] = selected_partitions["table"].isin(available_partitions["table_name"])
        invalid_tables = selected_partitions[~selected_partitions["is_valid_table"]]
        if not invalid_tables.empty:
            logger.warning(f"The following tables, for which partitions were selected, are not selected: {invalid_tables['table'].unique().tolist()}")
        
        # Valid tables with explicit partitions to refresh
        selected_partitions = selected_partitions[selected_partitions["is_valid_table"]]

        # If none of the tables with selected partitions are available, return all current partitions
        if selected_partitions.empty:
            return available_partitions

        # Identify the available tables for which partitions have been selected
        available_partitions["table_with_selected_partitions"] = available_partitions["table_name"].isin(selected_partitions["table"])
        
        # Outer merge to find: (1) valid partitions, (2) invalid partitions requested
        valid_partitions: pd.DataFrame = available_partitions.merge(
            selected_partitions[["table", "partition"]],
            left_on=["table_name", "partition_name"],
            right_on=["table", "partition"],
            how="outer",
            indicator=True
        )

        # If any of the selected partitions do not match the available partitions for the table
        invalid_partitions = valid_partitions[valid_partitions["_merge"] == "right_only"]
        if not invalid_partitions.empty:
            logger.warning(f"Invalid partitions found:\n{invalid_partitions[['table', 'partition']].to_json(orient='records')}")

        # Partitions to be refreshed
        # 1. All partitions from related tables without selected partitions
        # 2. Partitions from tables with selected partitions
        partitions = valid_partitions[
            (
                (valid_partitions["_merge"] == "left_only")
                & (valid_partitions["table_with_selected_partitions"] == False)
            )
            | (valid_partitions["_merge"] == "both")
        ][["table_name", "partition_name"]]
        logger.info(f"Partitions to refresh: {partitions.to_json(orient='records')}")
        
        return partitions

# METADATA ********************

# META {
# META   "language": "python",
# META   "language_group": "jupyter_python"
# META }

# CELL ********************

def refresh() -> None:
    """
    Refresh specified tables and partitions in a Power BI dataset.
    
    Raises:
        ValueError: If invalid tables or partitions are specified.
        RuntimeError: If the refresh operation fails.
        Exception: If dataset operations fail.
    """
    
    dataset: Dataset = Dataset(workspace_id, dataset_id)

    logger.info(f"Refreshing the '{dataset.dataset_name}' dataset in workspace '{dataset.workspace_name}'...")
    
    try:
        logger.info("Getting tables to refresh...")
        tables: pd.DataFrame = get_tables(dataset, tables_to_refresh)

        logger.info("Getting partitions to refresh...")
        partitions: pd.DataFrame = (
            get_partitions(dataset, tables, partitions_to_refresh)
            .rename(columns={"table_name": "table", "partition_name": "partition"})
        )
    except Exception as e:
        logger.error(f"Failed to retrieve tables and partitions: {str(e)}")
        raise

    try:
        logger.info(f"Requesting refresh for objects: {partitions.to_json(orient='records')}")
        
        refresh_request_id: str = dataset.refresh_objects(partitions, commit_mode, max_parallelism)
        if not refresh_request_id:
            raise ValueError("Refresh request is invalid.")
        
        logger.info(f"Refresh request ID: {refresh_request_id}")
        
        if dataset.check_refresh_status(refresh_request_id) != "Completed":
            raise RuntimeError("Refresh failed. Check refresh history for more details.")
            
        logger.info("Refresh completed successfully.")
    except Exception as e:
        logger.error(f"Unexpected error during refresh: {str(e)}")
        raise

# METADATA ********************

# META {
# META   "language": "python",
# META   "language_group": "jupyter_python"
# META }

# CELL ********************

if __name__ == "__main__":
    refresh()

# METADATA ********************

# META {
# META   "language": "python",
# META   "language_group": "jupyter_python"
# META }
