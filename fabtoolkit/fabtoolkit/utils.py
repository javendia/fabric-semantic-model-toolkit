"""
Utilities module for fabtoolkit.

This module provides:
- Constants
- Utilities
"""

from dataclasses import dataclass
from datetime import date
from enum import StrEnum
from io import StringIO
import json
import pandas as pd

# ============================================================================
# CONSTANTS
# ============================================================================

class Interval(StrEnum):
    """Enum representing different time intervals."""

    YEAR = "YEAR"
    QUARTER = "QUARTER"
    MONTH = "MONTH"

@dataclass
class IntervalDefinition:
    """Data class representing the definition of a time interval.
    
    Attributes:
        start_interval (str): Pandas frequency alias for start of interval (e.g., 'YS', 'QS', 'MS').
            - 'YS': Year start
            - 'QS': Quarter start
            - 'MS': Month start
        end_interval (str): Pandas frequency alias for end of interval (e.g., 'YE', 'QE', 'ME').
            - 'YE': Year end
            - 'QE': Quarter end
            - 'ME': Month end
        offset (pd.DateOffset): Pandas DateOffset for the interval.
    """

    start_interval: str
    end_interval: str
    offset: pd.DateOffset

class Constants:
    """Class to hold constant values.
    
    Pandas frequency aliases:
        - 'YS'/'YE': Year start/end
        - 'QS'/'QE': Quarter start/end
        - 'MS'/'ME': Month start/end
    """

    DATE_FORMAT: str = "%Y%m%d"
    INTERVALS: dict[Interval, IntervalDefinition] = {
        Interval.YEAR: IntervalDefinition(
            start_interval='YS',  # Year start
            end_interval='YE',     # Year end
            offset=pd.offsets.YearBegin
        ),
        Interval.QUARTER: IntervalDefinition(
            start_interval='QS',  # Quarter start
            end_interval='QE',     # Quarter end
            offset=pd.offsets.QuarterBegin
        ),
        Interval.MONTH: IntervalDefinition(
            start_interval='MS',  # Month start
            end_interval='ME',     # Month end
            offset=pd.offsets.MonthBegin
        )
    }

# ============================================================================
# UTILITIES
# ============================================================================

def is_valid_text(value: str) -> bool:
    """
    Checks if the provided value is a valid non-empty string.

    Args:
        value (str): The value to check.
    
    Returns:
        bool: True if the value is a non-empty string, False otherwise.
    """
    
    return isinstance(value, str) and value.strip()

def validate_json(json_str: str, columns: list[str]) -> pd.DataFrame:
    """
    Validates a JSON string to ensure it contains the specified columns and no empty values.
    
    Args:
        json_str (str): JSON string to validate.
        columns (list[str]): List of expected column names.

    Returns:
        pd.DataFrame: DataFrame created from the JSON string.

    Raises:
        ValueError: If JSON is invalid, missing columns, contains empty values, or invalid inputs.
    """

    if not isinstance(json_str, str):
        raise ValueError(f"Invalid JSON input: must be a string, got {type(json_str).__name__}")
    if not columns or not isinstance(columns, list):
        raise ValueError("Invalid columns input: must be a non-empty list of column names.")

    try:
        df = pd.read_json(StringIO(json_str))
    except ValueError as e:
        raise ValueError(f"Malformed JSON data or parsing issue: {e}")

    missing = [col for col in columns if col not in df.columns]
    if missing:
        raise ValueError(f"Missing columns in JSON: {missing}")

    if df.isna().any().any():
        raise ValueError("Empty/null values found in JSON columns.")
    
    # Check for empty strings in object/string columns
    for col in df.select_dtypes(include=['object']).columns:
        if (df[col].astype(str).str.strip() == '').any():
            raise ValueError(f"Empty string values found in column '{col}'.")
        
    return df

def get_bounds_from_offset(
    min_date: date,
    end_date: date,
    interval: str,
    number_of_intervals: str
) -> tuple[date, date]:
    """
    Calculates the start and end dates based on the given interval and number of intervals.

    Args:
        min_date (date): The minimum date to consider.
        end_date (date): The end date for the range.
        interval (str): The interval of the date range ('YEAR', 'QUARTER', 'MONTH').
        number_of_intervals (str): The number of intervals to consider.
                If this value is *, the function returns min_date and end_date.

    Returns:
        tuple[date, date]: A tuple containing the start date and end date of the range as date objects.

    Raises:
        ValueError: If interval is invalid or if dates are not datetime objects.
    """

    if not isinstance(min_date, date):
        raise ValueError(f"Invalid minimum date value: {min_date}. Must be a datetime.date object.")
    if not isinstance(end_date, date):
        raise ValueError(f"Invalid end date value: {end_date}. Must be a datetime.date object.")

    try:
        interval_def = Constants.INTERVALS[Interval(interval.upper())]
        end_interval = interval_def.end_interval
        offset = interval_def.offset
    except (KeyError, ValueError):
        valid_intervals = ', '.join(str(i.value) for i in Interval)
        raise ValueError(f"Invalid interval value: {interval}. Expected one of: {valid_intervals}.")
    
    # Convert end_date to Period
    end_period_frequencies = {'YE': 'Y', 'QE': 'Q', 'ME': 'M'}
    end_period_freq = end_period_frequencies.get(end_interval)
    end_period = pd.Period(end_date, freq=end_period_freq).to_timestamp(how="end")

    if number_of_intervals == '*':
        start_date: date = min_date
    else:
        try:
            intervals = int(number_of_intervals)
        except (ValueError, TypeError):
            raise ValueError(f"Invalid number of intervals: {number_of_intervals}. Must be an integer.")
        
        if intervals <= 0:
            raise ValueError(f"Invalid number of intervals: {number_of_intervals}. Must be greater than 0.")

        # Subtract offset, and get start date
        start_date: date = (end_period - offset(intervals)).to_period(end_period_freq).start_time
        
        # Ensure start_date is not earlier than min_date
        start_date = max(start_date, min_date)

    return start_date.date(), end_period.date()

def generate_date_ranges(
    start_date: date,
    end_date: date,
    interval: str
) -> pd.DataFrame:
    """
    Generates date ranges based on the specified interval.

    Args:
        start_date (date): The start date for the range.
        end_date (date): The end date for the range.
        interval (str): The interval of the date range ('YEAR', 'QUARTER', 'MONTH').

    Returns:
        pd.DataFrame: DataFrame with 'range_start' and 'range_end' columns as date objects.

    Raises:
        ValueError: If start_date or end_date are not date/datetime objects, or if interval is invalid.
    """

    if not isinstance(start_date, date):
        raise ValueError(f"Invalid start date value: {start_date}. Must be a datetime.date object.")
    if not isinstance(end_date, date):
        raise ValueError(f"Invalid end date value: {end_date}. Must be a datetime.date object.")
    if start_date > end_date:
        raise ValueError(f"Invalid date range: Start date ({start_date}) must be less than or equal to end date ({end_date}).")

    try:
        interval_def = Constants.INTERVALS[Interval(interval.upper())]
        start_interval = interval_def.start_interval
        end_interval = interval_def.end_interval
    except (KeyError, ValueError):
        valid_intervals = ', '.join(str(i.value) for i in Interval)
        raise ValueError(f"Invalid interval value: {interval}. Expected one of: {valid_intervals}.")

    start_dates = pd.date_range(start_date, end_date, freq=start_interval).date.tolist()
    end_dates = pd.date_range(start_date, end_date, freq=end_interval).date.tolist()

    # Adding start date or end date if pd.date_range does not include them
    if start_dates[0] != start_date:
        start_dates.insert(0, start_date)
    if end_dates[-1] != end_date:
        end_dates.append(end_date)
    
    return pd.DataFrame({"range_start": start_dates, "range_end": end_dates})