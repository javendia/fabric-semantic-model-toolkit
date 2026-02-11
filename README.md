![Global Power Platform Bootcamp 2026](./resources/img/banner.jpeg)

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)
[![Python](https://img.shields.io/badge/Python-3.10+-blue.svg)](https://www.python.org/)

Repositorio de la ponencia **"Salvar al soldado Power BI: particiones y refrescos eficientes"**  
**Evento:** Global Power Platform Bootcamp 2026 (Alicante)

---

## 📖 Resumen

El objetivo de este proyecto es la implementación de un flujo de trabajo que permita crear particiones automáticamente en conjuntos de datos de Power BI, así como ofrezca la posibilidad de actualizar todo el conjunto de datos o únicamente las tablas / particiones que se consideren necesarias.

## 📦 Contenidos

La estructura del repositorio es la siguiente:

```
gppb2026/
├── /doc/                                   # Documentación adicional
├── /lib/                                   # Librerías personalizadas
    ├── fabtoolkit-1.0.0-py3-none-any.whl   # Conjunto de utilidades para trabajar con Microsoft Fabric
├── /resources/                             # Recursos adicionales (imágenes, ejemplos, etc.)
├── /src/                                   # Código fuente de la solución
│   ├── NB_PAR_ORCHESTRATOR.Notebook        # Orquestador principal
│   ├── NB_PAR_PARTITIONER.Notebook         # Particionamiento
│   └── NB_PAR_REFRESHER.Notebook           # Refresco de datos
├── LICENSE
└── README.md
```

| Elemento | Descripción |
|----------|-------------|
| **fabtoolkit-1.0.0-py3-none-any.whl** | Librería personalizada con funciones reutilizables para Microsoft Fabric |
| [**NB_PAR_ORCHESTRATOR.Notebook**](./src/PARTITIONS/NB_PAR_ORCHESTRATOR.Notebook/README.md) | Cuaderno principal que controla el flujo completo: orquesta el particionado y el refresco del conjunto de datos |
| [**NB_PAR_PARTITIONER.Notebook**](./src/PARTITIONS/NB_PAR_PARTITIONER.Notebook/README.md) | Genera particiones dinámicamente en función de criterios de fecha personalizables |
| [**NB_PAR_REFRESHER.Notebook**](./src/PARTITIONS/NB_PAR_REFRESHER.Notebook/README.md) | Ejecuta el refresco del conjunto de datos para un grupo de tablas / particiones especificadas |

Para más detalles sobre cada cuaderno, pulsa en los enlaces correspondientes arriba.

## 🗹 Prerrequisitos

- ✅ Una **capacidad de Microsoft Fabric** en el inquilino de Azure
- ✅ Un **área de trabajo de Fabric** asignada a la capacidad
- ✅ Permisos de **Colaborador o superior** en el área de trabajo
- ✅ [Permisos para crear artefactos de Fabric](https://learn.microsoft.com/es-es/fabric/admin/fabric-switch)
- ✅ Una cuenta de **GitHub** para alojar el repositorio

## 🚀 Instalación y configuración

1. Preparar el repositorio

```bash
# Opción A: Bifurcar en GitHub
# Ve a https://github.com/javendia/gppb2026 y haz clic en "Fork"

# Opción B: Clonar directamente
git clone https://github.com/javendia/gppb2026.git
cd gppb2026
```

2. Sincronizar con Fabric

    1. Navega al **área de trabajo de Microsoft Fabric**
    2. Ve a **Configuración > Integración con Git**
    3. Selecciona **GitHub** como proveedor de Git
    4. Conecta tu cuenta de GitHub y selecciona el repositorio bifurcado o clonado
    5. Selecciona la rama deseada (por ejemplo, **main**) y la carpeta raíz **src**
    6. Pulsa el botón **Conectar y sincronizar**

3. En el área de trabajo de Fabric, abre el cuaderno **NB_PAR_ORCHESTRATOR**
4. Importa la librería personalizada **fabtoolkit-1.0.0-py3-none-any.whl** entre los recursos integrados del cuaderno:

<p align="center">
    <img src="./resources/img/install-wheel.png" alt="Importar librería personalizada" style="max-width: 400px; height: auto; border-radius: 8px;">
</p>

> [!IMPORTANT]
> Fabric descargará todos los artefactos automáticamente

## 📚 Recursos y documentación

- [Documentación de Microsoft Fabric](https://learn.microsoft.com/es-es/fabric/)
- [SemPy](https://learn.microsoft.com/es-es/python/api/semantic-link-sempy/sempy.fabric?view=semantic-link-python)
- [NotebookUtils](https://learn.microsoft.com/es-es/fabric/data-engineering/notebook-utilities)

## 📜 Licencia
Este proyecto está bajo la Licencia MIT. Consulta el archivo [LICENSE](LICENSE) para más detalles.
