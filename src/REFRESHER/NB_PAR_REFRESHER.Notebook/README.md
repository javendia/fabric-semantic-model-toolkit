# NB_PAR_REFRESHER

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)
[![Microsoft Fabric](https://img.shields.io/badge/Microsoft-Fabric-blue)](https://www.microsoft.com/microsoft-fabric)
[![Python](https://img.shields.io/badge/Python-3.10+-blue.svg)](https://www.python.org/)

## 📋 Summary

The **NB_PAR_REFRESHER** notebook is responsible for **controlled execution of data refreshes on Power BI semantic models**. It allows users to specify specific entities and partitions to refresh, thus optimizing resource usage and reducing update times by avoiding unnecessary full refreshes.

Additionally, it provides a preconfigured approach for refreshing data in a memory-efficient manner, reducing peak memory consumption and enabling efficient execution on lower-capacity Microsoft Fabric SKUs and an option to refresh related tables of selected entities to maintain referential integrity.

---

## ➡️ Input parameters

### Basic configuration

| Parameter | Type | Description | Example |
|-----------|------|-------------|---------|
| `workspace_id` | string | GUID of the Microsoft Fabric workspace | `"dc1b17ac-1d39-4be3-a848-45c8a55c05f1"` |
| `dataset_id` | string | GUID of the Power BI semantic model | `"0e4e85ca-f446-44b6-bf18-2a9114668242"` |

### Refresh parameters

| Parameter | Type | Description | Example | Default |
|-----------|------|-------------|---------|---------|
| `tables_to_refresh` | string | Entities to refresh (comma-separated) | `"Customer,Sales"` | All entities |
| `partitions_to_refresh` | string (JSON) | Specific partitions to refresh | See table below | All partitions |
| `enable_referential_integrity` | boolean | Include tables related to the selected entities to maintain referential integrity throughout the refresh process. | `True`, `False` | `True` |
| `refresh_mode` | string | Mode of refresh execution | `"memory-optimized"`, `"custom"` | `"custom"` |
| `refresh_type` | string | Type of refresh to perform | `"full"`, `"clearValues"`, `"calculate"`, `"dataOnly"`, `"automatic"`, `"defragment"` | `"full"` |
| `commit_mode` | string | Transaction confirmation | `"transactional"`, `"partialBatch"` | `"transactional"` |
| `max_parallelism` | integer | Maximum number of entities to refresh in parallel | `6` | `4` |

#### `tables_to_refresh`

- **Format:** String with entity names separated by commas.

  ```plaintext
  "Customer,Product,Sales"
  ```

- **Behavior:**
  - If existing tables in the semantic model are provided, it refreshes only those entities along with their dependencies. 
    - If any entity does not exist, it is skipped and a warning is displayed.
    - If all provided entities are invalid, an error is shown and the process is aborted.
  - If empty, it refreshes all entities in the semantic model.

#### `partitions_to_refresh`

- **Format:** JSON of entities and partitions to refresh

```json
[
  {
    "table": "Sales",
    "selected_partitions": ["Sales_20250101_20250331", "Sales_20250401_20250630"]
  },
  {
    "table": "Orders",
    "selected_partitions": ["Orders_20250101_20251231"]
  }
]
```

- **Behavior:**
  - If a valid value is provided, it refreshes only the specified partitions.
    - If an entity appears in the `tables_to_refresh` parameter but not in `partitions_to_refresh`, all its partitions are refreshed.
    - If an entity appears in the `partitions_to_refresh` parameter, only the listed partitions are refreshed.
  - If empty, it refreshes all partitions of the selected entities.
  - If any table or partition does not exist, it is skipped and a warning is displayed.
---

#### `enable_referential_integrity`

- **Format:** Boolean (`True` or `False`)

- **Behavior:**
  - If `True`, it includes tables related to the selected entities to maintain referential integrity throughout the refresh process.

  ```python
  dataset.get_related_tables(["Sales"])
  # Returns: [Sales, Customer, Product, Store, etc.]
  # All entities with direct/indirect relationships
  ```

  - If `False`, only the explicitly selected tables are refreshed, without considering related tables.

#### `refresh_mode`

- **Format:** String (`"custom"` or `"memory-optimized"`)

- **Behavior:**
  - If `"custom"`, it uses the specified `refresh_type`, `commit_mode`, and `max_parallelism` for the refresh process.
  - If `"memory-optimized"`, it follows these three sequential operations:
    1. `clearValues` removes the existing data from the selected objects.
    2. `dataOnly` loads data from the source, using `partialBatch` commit mode and a parallelism of `1`.
    3. `calculate` recalculates the selected objects after the data has been loaded.

## 🔄 Action flow

```mermaid
flowchart TD
  A["Start: run()"] --> B["Create Dataset and read metadata"]
  B --> C{"tables_to_refresh provided?"}

  C -->|No| D["Select all dataset tables"]
  C -->|Yes| E["Parse table names and validate"]
  E --> F{"Any invalid table names?"}
  F -->|Yes| G["Warn and omit invalid names"]
  F -->|No| H["Keep provided tables"]
  G --> I{"Any valid tables remain?"}
  I -->|No| ERR["Abort with error"]
  I -->|Yes| J{"enable_referential_integrity?"}
  H --> J
  J -->|Yes| K["Include related tables"]
  J -->|No| L["Use selected tables only"]
  D --> M["Tables selected"]
  K --> M
  L --> M

  M --> N{"partitions_to_refresh provided?"}
  N -->|No| O["Select all partitions of selected tables"]
  N -->|Yes| P["Parse requested tables and partitions"]
  P --> Q["Warn and omit tables not selected"]
  Q --> R{"Any requested tables remain?"}
  R -->|No| O
  R -->|Yes| S["Validate requested partitions"]
  S --> T["Warn and omit invalid partitions"]
  T --> U["Keep requested partitions and all partitions for other selected tables"]
  O --> V["Partitions selected"]
  U --> V

  V --> W{"refresh_mode is memory-optimized?"}
  W -->|No| X["Request refresh using refresh_type, commit_mode, and max_parallelism"]
  W -->|Yes| Y["Request clearValues"]
  Y --> Z{"Request ID returned and status is Completed?"}
  Z -->|No| ERR
  Z -->|Yes| AA["Request dataOnly<br/>partialBatch, parallelism 1"]
  AA --> AB{"Request ID returned and status Completed?"}
  AB -->|No| ERR
  AB -->|Yes| AC["Request calculate"]
  AC --> AD{"Request ID returned and status is Completed?"}
  AD -->|No| ERR
  AD -->|Yes| END["Refresh completed"]

  X --> AE{"Request ID returned and status is Completed?"}
  AE -->|No| ERR
  AE -->|Yes| END

  style A fill:#90EE90,color:#000
  style END fill:#87CEEB,color:#000
  style ERR fill:#FFB6C6,color:#000
  style G fill:#FFD580,color:#000
  style Q fill:#FFD580,color:#000
  style T fill:#FFD580,color:#000
  style Y fill:#FFE4B5,color:#000
  style AA fill:#FFE4B5,color:#000
  style AC fill:#FFE4B5,color:#000
```

---

### External libraries

- **pandas**: DataFrame manipulation.
- **logging**: Logging system.
- **sys**: Exception handling and program output.
- **typing**: Types (List, Optional).
- **StringIO**: Handling strings as files.

### fabtoolkit

Custom utilities toolkit to facilitate common operations in Microsoft Fabric. For more information about the bookstore, click the following [**link**](./../../../fabtoolkit/README.md).

The notebook uses the following functions from the `fabtoolkit` library:

```python
from fabtoolkit.utils import (
    is_valid_text          # Validate non-empty string
)
from fabtoolkit.log import ConsoleLogFormatter    # Custom logging format
from fabtoolkit.dataset import Dataset         # Class for operations on semantic models
```

---

## Usage examples

### Example 1: Refresh all entities and partitions

```python
tables_to_refresh = None
partitions_to_refresh = None
enable_referential_integrity = False
refresh_mode = "custom"
refresh_type = "full"
commit_mode = "transactional"
max_parallelism = 4
```

### Example 2: Refresh only one entity and all its partitions

```python
tables_to_refresh = "Sales"
partitions_to_refresh = None
enable_referential_integrity = False
refresh_mode = "custom"
refresh_type = "full"
commit_mode = "transactional"
max_parallelism = 4
```

### Example 3: Refresh only one entity and specific partitions

```python
tables_to_refresh = "Sales"
partitions_to_refresh = '[
  {
    "table": "Sales",
    "selected_partitions": ["Sales_20250101_20250331", "Sales_20250401_20250630"]
  }
]'
enable_referential_integrity = False
refresh_mode = "custom"
refresh_type = "full"
commit_mode = "transactional"
max_parallelism = 4
```

### Example 4: Refresh with referential integrity enabled

```python
tables_to_refresh = "Sales"
partitions_to_refresh = None
enable_referential_integrity = True
refresh_mode = "custom"
refresh_type = "full"
commit_mode = "transactional"
max_parallelism = 4
```

### Example 5: Memory-optimized refresh

```python
tables_to_refresh = "Sales"
partitions_to_refresh = None
enable_referential_integrity = True
refresh_mode = "memory-optimized"
```

---