[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](../../LICENSE)
[![Python](https://img.shields.io/badge/Python-3.10+-blue.svg)](https://www.python.org/)

# fabtoolkit

A utility library designed to reuse common tasks when working with **Microsoft Fabric** semantic models. Simplify dataset operations, logging, and data processing with a comprehensive toolkit.

---

## Overview

**fabtoolkit** provides a collection of Python utilities to develop workflows in Microsoft Fabric. It includes modules for semantic model management, logging and common data processing tasks.

---

## Modules

### [dataset.py](./fabtoolkit/dataset.py)
Provides the `Dataset` class for programmatic interaction with Fabric semantic models.

**Features:**
- Load semantic model metadata (tables, columns, partitions, relationships).
- Analyze model structure and dependencies.
- Work with dataset properties and configurations.

**Example:**
```python
from fabtoolkit.dataset import Dataset

# Initialize with workspace and dataset IDs
dataset = Dataset(workspace_id="your-workspace-id", dataset_id="your-dataset-id")

# Access tables and partitions
print(dataset.tables)
print(dataset.partitions)
```

---

### [log.py](./fabtoolkit/log.py)
Provides `ConsoleLogFormatter` for color-coded console logging.

**Features:**
- ANSI color coding based on log levels (DEBUG, INFO, WARNING, ERROR, CRITICAL).
- Custom date/time formatting.
- Enhanced readability of log output.

**Example:**
```python
import logging
from fabtoolkit.log import ConsoleLogFormatter

# Create logger with custom formatter
logger = logging.getLogger(__name__)
handler = logging.StreamHandler()
handler.setFormatter(ConsoleLogFormatter())
logger.addHandler(handler)
logger.setLevel(logging.DEBUG)

# Log messages with color coding
logger.info("Operation started")
logger.warning("Check this condition")
logger.error("An error occurred")
```

---

### [utils.py](./fabtoolkit/utils.py)
Provides utility functions and constants for common operations.

**Features:**
#### Constants
- **`Interval` enum**: Represents time intervals (YEAR, QUARTER, MONTH).
- **`IntervalDefinition` dataclass**: Defines interval properties using Pandas frequency aliases.
- **`Constants` class**: Centralized configuration for date formatting and interval definitions.

#### Functions
- **`is_valid_text(value: str) -> bool`**: Validates if a value is a non-empty string.
- **`validate_json(json_str: str, columns: list[str]) -> pd.DataFrame`**: Validates JSON strings and converts them to DataFrames with schema validation.

**Example:**
```python
from fabtoolkit.utils import is_valid_text, validate_json, Constants, Interval

# Validate text
is_valid = is_valid_text("  ")  # False
is_valid = is_valid_text("hello")  # True

# Access interval definitions
month_interval = Constants.INTERVALS[Interval.MONTH]
print(month_interval.start_interval)  # 'MS'

# Validate JSON data
json_str = '{"name": "John", "age": 30}'
df = validate_json(json_str, columns=["name", "age"])
```

---

## Requirements

- **Python**: 3.10 or higher
- **Dependencies**:
  - `pandas`: Data manipulation and analysis
  - `semantic-link`: SemPy library for Fabric semantic models
  - `semantic-link-labs`: Extended semantic model utilities

---

## Installation

1. Download the `.whl` file from `/fabtoolkit/dist/`
2. In your Fabric notebook, go to **Settings > Built-in resources**
3. Upload the wheel file
4. Import in your notebook:
   ```python
   from fabtoolkit.dataset import Dataset
   from fabtoolkit.log import ConsoleLogFormatter
   from fabtoolkit.utils import *
   ```

---

## 💡 Usage examples

### Example 1: Analyze a Semantic Model

```python
from fabtoolkit.dataset import Dataset
import pandas as pd

# Load semantic model
dataset = Dataset(
    workspace_id="abc123-workspace-id",
    dataset_id="def456-dataset-id"
)

# Get all tables
tables = dataset.tables
print(f"Tables: {tables['table_name'].unique()}")

# Get relationships
relationships = dataset.relationships
print(relationships)
```

### Example 2: Set up logging

```python
import logging
from fabtoolkit.log import ConsoleLogFormatter

# Configure logger
logger = logging.getLogger("fabric-app")
console_handler = logging.StreamHandler()
console_handler.setFormatter(ConsoleLogFormatter())
logger.addHandler(console_handler)
logger.setLevel(logging.INFO)

# Use throughout your application
logger.info("Starting process...")
logger.warning("This is a warning message")
logger.error("An error occurred")
```

### Example 3: Work with time intervals

```python
from fabtoolkit.utils import Constants, Interval
import pandas as pd

# Get interval configuration
month_def = Constants.INTERVALS[Interval.MONTH]

# Use in date range calculations
dates = pd.date_range(start="2024-01-01", periods=12, freq=month_def.start_interval)
print(dates)
```

---

## 📖 Documentation

For more information:
- [Microsoft Fabric documentation](https://learn.microsoft.com/en-us/fabric/)
- [SemPy documentation](https://learn.microsoft.com/en-us/python/api/semantic-link-sempy/sempy.fabric)

---

## 📜 License

This project is licensed under the MIT License. See the [LICENSE](./../LICENSE) file for more details.