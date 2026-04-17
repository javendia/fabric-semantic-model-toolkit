import sempy.fabric as fabric
import pandas as pd
import re
from sempy_labs.tom import connect_semantic_model
import networkx as nx
import time
from typing import Optional

class Dataset:
    """
    Represents a semantic model in Fabric.
    
    Attributes:
        workspace_name (str): Name of the workspace.
        dataset_name (str): Name of the dataset.
        workspace_id (str): Identifier of the workspace.
        dataset_id (str): Identifier of the dataset.
        tables (pd.DataFrame): DataFrame containing tables and columns information.
        partitions (pd.DataFrame): DataFrame containing partitions information.
        relationships (pd.DataFrame): DataFrame containing relationships information.
    """

    def __init__(self, workspace_id: str, dataset_id: str):

        if not workspace_id or not dataset_id:
            raise ValueError("Workspace and dataset identifiers must be provided.")
        
        # Private attributes
        self.__workspace_id = workspace_id
        self.__dataset_id = dataset_id

        # Resolve workspace and dataset names from their IDs
        self.__workspace_name = fabric.resolve_workspace_name(self.__workspace_id)
        self.__dataset_name = fabric.resolve_dataset_name(workspace=self.__workspace_id, dataset_id=self.__dataset_id)

        # Retrieve tables and columns
        tables = fabric.list_columns(
            workspace=self.__workspace_id, dataset=self.__dataset_id)
        
        if tables.empty:
            raise ValueError(f"Dataset '{self.__dataset_name}' in workspace '{self.__workspace_name}' contains no tables.")

        self.__tables = tables.rename(columns=lambda x: x.lower().replace(" ", "_"))
        
        # Retrieve partitions
        partitions = fabric.list_partitions(
            workspace=self.__workspace_id, dataset=self.__dataset_id)
        self.__partitions = partitions.rename(columns=lambda x: x.lower().replace(" ", "_"))

        # Retrieve relationships
        relationships = fabric.list_relationships(
            workspace=self.__workspace_id, dataset=self.__dataset_id)
        
        if relationships.empty:
            raise ValueError(f"Dataset '{self.__dataset_name}' in workspace '{self.__workspace_name}' contains no relationships.")
        
        self.__relationships = relationships.rename(columns=lambda x: x.lower().replace(" ", "_"))
        
    @property
    def workspace_name(self) -> str:
        """Workspace name."""
        return self.__workspace_name
    
    @property
    def dataset_name(self) -> str:
        """Dataset name."""
        return self.__dataset_name
    
    @property
    def workspace_id(self) -> str:
        """Workspace identifier."""
        return self.__workspace_id
    
    @property
    def dataset_id(self) -> str:
        """Dataset identifier."""
        return self.__dataset_id
    
    @property
    def tables(self) -> pd.DataFrame:
        """DataFrame with tables and columns information."""
        return self.__tables.copy()
    
    @property
    def partitions(self) -> pd.DataFrame:
        """DataFrame with partitions information."""
        return self.__partitions.copy()
    
    @property
    def relationships(self) -> pd.DataFrame:
        """DataFrame with relationships information."""
        return self.__relationships.copy()
    
    def create_m_partitions(self, partitions: pd.DataFrame) -> None:
        """
        Creates M partitions in the semantic model.

        Args:
            partitions (pd.DataFrame): Partitions information with columns: ['table_name', 'partition_name', 'query_definition']

        Returns:
            None

        Raises:
            ValueError: If required columns are missing from the DataFrame.
        """
        required_columns = {'table_name', 'partition_name', 'query_definition'}
        missing = required_columns - set(partitions.columns)
        if missing:
            raise ValueError(f"Missing required columns to create M partitions: {missing}")
        
        try:
            with connect_semantic_model(dataset=self.__dataset_name, readonly=False, workspace=self.__workspace_name) as tom:
                for row in partitions.itertuples():
                    tom.add_m_partition(
                        table_name=row.table_name,
                        partition_name=row.partition_name,
                        expression=row.query_definition,
                        mode="Import"
                    )
        except Exception as e:
            raise RuntimeError(f"Failed to create M partitions: {e}") from e

    def delete_default_partition(self, table: str) -> None:
        """
        Deletes the default partition for a table.

        Args:
            table (str): The table name.

        Returns:
            None
        """

        tmsl_script = {
            "delete": {
                "object": {
                    "database": self.__dataset_name,
                    "table": table,
                    "partition": table
                }
            }
        }

        fabric.execute_tmsl(workspace=self.__workspace_id, script=tmsl_script)

    @staticmethod
    def extract_query_definition(query: str) -> tuple[str, str]:
        """
        Extracts the base query and last step name from a partition query definition.

        Args:
            query (str): The partition query definition in M language.

        Returns:
            tuple[str, str]: Tuple of (base_query, last_step_name)

        Raises:
            ValueError: If query format is invalid or required elements not found.
        """
        if not query or not isinstance(query, str):
            raise ValueError("Query must be a non-empty string.")

        # Find the 'in' keyword line
        m = re.search(r'\n[ \t]*in[ \t]*\n', query)
        idx = m.start()

        lines = query[:idx].splitlines()
        # Regex to identify partition definition lines. The pattern matches lines like:
        #    TableName_YYYYMMDD_YYYYMMDD =
        partition_line_regex = r'^\s*\w+_\d{8}_\d{8}\s*='

        filtered_lines = []
        for line in lines:
            if re.match(partition_line_regex, line):
                # Remove comma from previous line if present
                if filtered_lines and filtered_lines[-1].endswith(','):
                    filtered_lines[-1] = filtered_lines[-1][:-1]
                continue
            filtered_lines.append(line)

        base_query = '\n'.join(filtered_lines)
        last_step = filtered_lines[-1].lstrip().split(' ')[0]

        return base_query, last_step

    def get_related_tables(self, tables: list[str]) -> pd.DataFrame:
        """
        Gets all related tables (ancestors and specified tables) for refresh.

        Args:
            tables (list[str]): List of table names to refresh.

        Returns:
            pd.DataFrame: DataFrame with all related tables for refresh.
        """

        G = nx.DiGraph()
        for row in self.__relationships.itertuples():
            G.add_edge(row.to_table, row.from_table)

        refresh_set = set()
        for t in tables:
            # Disconnected tables
            if t not in G:
                refresh_set.add(t)
            # Dimension tables
            elif G.in_degree(t) == 0:
                refresh_set.add(t)
            # Snowflake or fact tables
            else:
                refresh_set.update(nx.ancestors(G, t))
                refresh_set.add(t)
        
        return pd.DataFrame({"table_name": list(refresh_set)})

    def refresh_objects(
            self, 
            df: pd.DataFrame, 
            commit_mode: Optional[str] = "transactional", 
            max_parallelism: Optional[int] = 4
        ) -> str:
        """
        Refresh specified objects in the dataset.

        Args:
            df (pd.DataFrame): DataFrame with columns: ['table', 'partition'] specifying objects to refresh.
            commit_mode (str): Determines if objects will be committed in batches or only when complete.
            max_parallelism (int): The maximum number of threads on which to run parallel processing commands

        Returns:
            str: Refresh request identifier (UUID string) to track refresh progress. Use this identifier with
                 check_refresh_status() to monitor the refresh operation status.

        Raises:
            ValueError: If DataFrame is empty or missing required columns.
            TypeError: If input is not a DataFrame.
        """
        # Validate input DataFrame
        if not isinstance(df, pd.DataFrame):
            raise TypeError(f"Expected pd.DataFrame, got {type(df).__name__}")
        if df.empty:
            raise ValueError("DataFrame cannot be empty")
        
        required_columns = {'table', 'partition'}
        missing = required_columns - set(df.columns)
        if missing:
            raise ValueError(f"Missing required columns: {missing}")
        
        # Validate commit mode
        available_commit_modes = {"transactional", "partialBatch"}
        if commit_mode not in available_commit_modes:
            raise ValueError(f"Invalid commit mode '{commit_mode}'. Available modes: {available_commit_modes}")
        
        # Validate max parallelism
        if not isinstance(max_parallelism, int) or max_parallelism <= 0:
            raise ValueError("Max parallelism value must be a positive integer.")

        objects = df.to_dict(orient="records")

        refresh_request_id = fabric.refresh_dataset(
            workspace=self.__workspace_id,
            dataset=self.__dataset_id,
            objects=objects,
            refresh_type="full",
            apply_refresh_policy=False,
            commit_mode=commit_mode,
            max_parallelism=max_parallelism
        )

        return refresh_request_id

    def check_refresh_status(self, refresh_request_id: str, timeout: int = 7200) -> str:
        """
        Check the status of a refresh operation with exponential decreasing backoff.

        Polls the refresh status periodically with exponential decreasing backoff:
        - Starts with 60s wait time for infrequent polling
        - Exponentially decreases to 10s minimum for more frequent polling as time progresses

        Args:
            refresh_request_id (str): The refresh request identifier to check.
            timeout (int, optional): Maximum time to wait for completion in seconds. Defaults to 7200 (2 hours).

        Returns:
            str: Final status of the refresh operation (e.g., 'Completed', 'Failed', 'Unknown').

        Raises:
            TimeoutError: If refresh operation does not complete within the timeout period.
            RuntimeError: If unable to retrieve refresh status from the API.
        """
        
        start_time = time.time()
        status = None
        max_backoff_seconds = 60    # 60 seconds initial wait
        min_backoff_seconds = 10    # 10 seconds minimum wait
        total_elapsed = 0
        
        while total_elapsed < timeout:
            try:
                status = fabric.get_refresh_execution_details(
                    workspace=self.__workspace_id,
                    dataset=self.__dataset_id,
                    refresh_request_id=refresh_request_id
                ).status
                
                if status != "Unknown":
                    return status
            except Exception as e:
                raise RuntimeError(f"Failed to retrieve refresh status: {e}") from e
            
            # Exponential decreasing backoff: decay from max to min
            elapsed_ratio = total_elapsed / timeout
            wait_time = max(
                min_backoff_seconds,
                max_backoff_seconds * (2 ** (-elapsed_ratio * 3))
            )
            time.sleep(wait_time)
            total_elapsed = time.time() - start_time
        
        raise TimeoutError(f"Refresh operation did not complete within {timeout} seconds. Last status: {status}")