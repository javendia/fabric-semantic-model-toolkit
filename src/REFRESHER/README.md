[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)
[![Python](https://img.shields.io/badge/Python-3.10+-blue.svg)](https://www.python.org/)

## 📋 Summary

This framework automatically creates date-based partitions and enables granular refresh workflows, allowing you to update only changed data instead of reprocessing your entire dataset.

**How it works:**
- 📅 **Automatic date-range partitioning**: Generates partitions by year, quarter, or month based on your data strategy.
- 🎯 **Granular refresh scope**: Refresh complete tables, table partitions within a date range, or specific partitions individually.
- 🔄 **Flexible orchestration**: Choose to partition, refresh, or both—independent operations.

| Component | Description |
|-----------|-------------|
| [**NB_PAR_ORCHESTRATOR**](./../../src/REFRESHER/NB_PAR_ORCHESTRATOR.Notebook/README.md) | Main notebook that controls the complete flow: orchestrates the partitioning and dataset refresh |
| [**NB_PAR_PARTITIONER**](./../../src/REFRESHER/NB_PAR_PARTITIONER.Notebook/README.md) | Dynamically generates partitions based on customizable date criteria |
| [**NB_PAR_REFRESHER**](./../../src/REFRESHER/NB_PAR_REFRESHER.Notebook/README.md) | Executes the dataset refresh for a specified group of tables / partitions |

Full documentation for each notebook is available by clicking on the corresponding links above.

---

## 📦 Dependencies

### External libraries

- **pandas**: DataFrame manipulation.
- **datetime**: Date calculations.
- **typing**: Types (Optional, Any, Dict).
- **logging**: Logging system.
- **sempy**: Microsoft Fabric semantic model interaction.
- **sempy_labs**: Extended utilities for Semantic Link.
- **notebookutils**: Built-in package for performing common tasks in Microsoft Fabric notebooks.
- **StringIO**: Handling strings as files.
- **uuid**: Generation of unique identifiers.
- **numpy**: Numerical operations and array handling.

### fabtoolkit

Custom utilities toolkit to facilitate common operations in Microsoft Fabric. For more information, see the [fabtoolkit documentation](./../../fabtoolkit/README.md).

---

## 🗹 Prerequisites

- ✅ A **Microsoft Fabric capacity** in your Azure tenant.
- ✅ A **Fabric workspace** assigned to the capacity.
- ✅ **Admin** permissions in the workspace.
- ✅ [Permissions to create Fabric artifacts](https://learn.microsoft.com/en-us/fabric/admin/fabric-switch).
- ✅ A **GitHub account** to host the repository.

---

## 🚀 Installation and setup

1. **Fork the repository on GitHub**

    1. Navigate to https://github.com/javendia/fabric-semantic-model-toolkit.
    2. Click the **Fork** button to create a copy of the repository in your GitHub account.

2. **Synchronize with Fabric**

    1. Navigate to your **Microsoft Fabric workspace**.
    2. Go to **Settings > Git integration**.
    3. Select **GitHub** as the Git provider.
    4. Connect your GitHub account and select the forked or cloned repository.
    5. Select your desired branch (e.g., **main**) and root folder **src**.
    6. Click the **Connect and sync** button.

3. **Import the fabtoolkit library**
   - In your Fabric workspace, open the **NB_PAR_ORCHESTRATOR** notebook.
   - Import the custom library [**fabtoolkit-1.0.0-py3-none-any.whl**](./../../fabtoolkit/dist/fabtoolkit-1.0.0-py3-none-any.whl) among the notebook's built-in resources:

   <p align="center">
       <img src="./../../resources/img/install-wheel.png" alt="Import custom library" style="max-width: 400px; height: auto; border-radius: 8px;">
   </p>

4. **Configure the parameters**
   - Review the configuration in the **NB_PAR_ORCHESTRATOR** notebook.
   - Update parameters based on your requirements:
     - Partitioning strategy (YEAR, QUARTER, MONTH).
     - Tables and date columns to partition.
     - Refresh scope and parallelism settings.
   - Refer to the notebook documentation for example configurations.

5. **Execute the orchestrator**
   - Run the **NB_PAR_ORCHESTRATOR** notebook.
   - The orchestrator will automatically invoke the partitioner and refresher notebooks in the correct sequence.