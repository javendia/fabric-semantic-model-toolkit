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

## 🛠️ Tools

### [REFRESHER](./src/REFRESHER/README.md)
A dynamic partitioning and refresh solution for Power BI semantic models, designed to optimize data refresh processes by creating and refreshing partitions based on user-defined criteria.

---

## 📚 Resources and documentation

- [Microsoft Fabric Documentation](https://learn.microsoft.com/en-us/fabric/)
- [SemPy](https://learn.microsoft.com/en-us/python/api/semantic-link-sempy/sempy.fabric?view=semantic-link-python)
- [NotebookUtils](https://learn.microsoft.com/en-us/fabric/data-engineering/notebook-utilities)

---

## 📜 License
This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for more details.