[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)
[![Python](https://img.shields.io/badge/Python-3.10+-blue.svg)](https://www.python.org/)

A comprehensive toolkit for operating, managing, and automating tasks on Power BI semantic models, including partitioning, data refreshes, and more.

---

## 📦 Contents

The repository structure is as follows:

```
fabric-semantic-model-toolkit/
├── /docs/                                      # Additional documentation
├── /fabtoolkit/                                # Custom libraries
    ├── dist/fabtoolkit-1.0.0-py3-none-any.whl  # Utilities toolkit for working with Microsoft Fabric
├── /resources/                                 # Additional resources (images, examples, etc.)
├── /src/                                       # Source code
│   ├── REFRESHER/                              # Dynamic partitioning and refresh solution
├── LICENSE
└── README.md
```

### 🔄 REFRESHER

This solution provides a framework for managing dynamic partitioning and data refresh of datasets in Microsoft Fabric.

| Component | Description |
|-----------|-------------|
| [**NB_PAR_ORCHESTRATOR.Notebook**](./src/REFRESHER/NB_PAR_ORCHESTRATOR.Notebook/README.md) | Main notebook that controls the complete flow: orchestrates the partitioning and dataset refresh |
| [**NB_PAR_PARTITIONER.Notebook**](./src/REFRESHER/NB_PAR_PARTITIONER.Notebook/README.md) | Dynamically generates partitions based on customizable date criteria |
| [**NB_PAR_REFRESHER.Notebook**](./src/REFRESHER/NB_PAR_REFRESHER.Notebook/README.md) | Executes the dataset refresh for a specified group of tables / partitions |

For more details on each notebook, click on the corresponding links above.

## 🗹 Prerequisites

- ✅ A **Microsoft Fabric capacity** in your Azure tenant
- ✅ A **Fabric workspace** assigned to the capacity
- ✅ **Contributor** or higher permissions in the workspace
- ✅ [Permissions to create Fabric artifacts](https://learn.microsoft.com/en-us/fabric/admin/fabric-switch)
- ✅ A **GitHub account** to host the repository

## 🚀 Installation and setup

1. Fork the repository on GitHub

    1. Navigate to https://github.com/javendia/fabric-semantic-model-toolkit
    2. Click the **Fork** button to create a copy of the repository in your GitHub account.

2. Synchronize with Fabric

    1. Navigate to your **Microsoft Fabric workspace**
    2. Go to **Settings > Git integration**
    3. Select **GitHub** as the Git provider
    4. Connect your GitHub account and select the forked or cloned repository
    5. Select your desired branch (e.g., **main**) and root folder **src**
    6. Click the **Connect and sync** button

> [!IMPORTANT]
> Fabric will automatically download all artifacts

3. **(Optional)** If you want to use the partitioning and dynamic refresh utility, additional configuration is required:

    1. In your Fabric workspace, open the **NB_PAR_ORCHESTRATOR** notebook
    2. Import the custom library [**fabtoolkit-1.0.0-py3-none-any.whl**](./fabtoolkit/README.md) among the notebook's built-in resources:

<p align="center">
    <img src="./resources/img/install-wheel.png" alt="Import custom library" style="max-width: 400px; height: auto; border-radius: 8px;">
</p>

## 📚 Resources and documentation

- [Microsoft Fabric Documentation](https://learn.microsoft.com/en-us/fabric/)
- [SemPy](https://learn.microsoft.com/en-us/python/api/semantic-link-sempy/sempy.fabric?view=semantic-link-python)
- [NotebookUtils](https://learn.microsoft.com/en-us/fabric/data-engineering/notebook-utilities)

## 📜 License
This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for more details.
