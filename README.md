[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)
[![Python](https://img.shields.io/badge/Python-3.10+-blue.svg)](https://www.python.org/)

Conjunto de herramientas para operar, gestionar y automatizar tareas sobre modelos semánticos de Power BI como particionado, refresco de datos, etc.

---

## 📦 Contenidos

La estructura del repositorio es la siguiente:

```
fabric-semantic-model-toolkit/
├── /docs/                                  # Documentación adicional
├── /lib/                                   # Librerías personalizadas
    ├── fabtoolkit-1.0.0-py3-none-any.whl   # Conjunto de utilidades para trabajar con Microsoft Fabric
├── /resources/                             # Recursos adicionales (imágenes, ejemplos, etc.)
├── /src/                                   # Código fuente
│   ├── REFRESHER/                          # Solución de particionado y refresco dinámico
├── LICENSE
└── README.md
```

### 🔄 REFRESHER

Esta solución proporciona un marco de trabajo para gestionar el particionado y refresco dinámico de conjuntos de datos en Microsoft Fabric.

| Elemento | Descripción |
|----------|-------------|
| [**NB_PAR_ORCHESTRATOR.Notebook**](./src/REFRESHER/NB_PAR_ORCHESTRATOR.Notebook/README.md) | Cuaderno principal que controla el flujo completo: orquesta el particionado y el refresco del conjunto de datos |
| [**NB_PAR_PARTITIONER.Notebook**](./src/REFRESHER/NB_PAR_PARTITIONER.Notebook/README.md) | Genera particiones dinámicamente en función de criterios de fecha personalizables |
| [**NB_PAR_REFRESHER.Notebook**](./src/REFRESHER/NB_PAR_REFRESHER.Notebook/README.md) | Ejecuta el refresco del conjunto de datos para un grupo de tablas / particiones especificadas |

Para más detalles sobre cada cuaderno, pulsa en los enlaces correspondientes arriba.

## 🗹 Prerrequisitos

- ✅ Una **capacidad de Microsoft Fabric** en el inquilino de Azure
- ✅ Un **área de trabajo de Fabric** asignada a la capacidad
- ✅ Permisos de **Colaborador o superior** en el área de trabajo
- ✅ [Permisos para crear artefactos de Fabric](https://learn.microsoft.com/es-es/fabric/admin/fabric-switch)
- ✅ Una cuenta de **GitHub** para alojar el repositorio

## 🚀 Instalación y configuración

1. Bifurcar el repositorio en GitHub

    1. Navega a https://github.com/javendia/fabric-semantic-model-toolkit
    2. Haz clic en el botón **Fork** para crear una copia del repositorio en tu cuenta de GitHub.

2. Sincronizar con Fabric

    1. Navega al **área de trabajo de Microsoft Fabric**
    2. Ve a **Configuración > Integración con Git**
    3. Selecciona **GitHub** como proveedor de Git
    4. Conecta tu cuenta de GitHub y selecciona el repositorio bifurcado o clonado
    5. Selecciona la rama deseada (por ejemplo, **main**) y la carpeta raíz **src**
    6. Pulsa el botón **Conectar y sincronizar**

> [!IMPORTANT]
> Fabric descargará todos los artefactos automáticamente

3. **(Opcional)** En el caso de querer emplear la utilidad de particionamiento y refresco dinámico, es necesario llevar a cabo una configuración adicional:

    1. En el área de trabajo de Fabric, abre el cuaderno **NB_PAR_ORCHESTRATOR**
    2. Importa la librería personalizada **fabtoolkit-1.0.0-py3-none-any.whl** entre los recursos integrados del cuaderno:

<p align="center">
    <img src="./resources/img/install-wheel.png" alt="Importar librería personalizada" style="max-width: 400px; height: auto; border-radius: 8px;">
</p>

## 📚 Recursos y documentación

- [Documentación de Microsoft Fabric](https://learn.microsoft.com/es-es/fabric/)
- [SemPy](https://learn.microsoft.com/es-es/python/api/semantic-link-sempy/sempy.fabric?view=semantic-link-python)
- [NotebookUtils](https://learn.microsoft.com/es-es/fabric/data-engineering/notebook-utilities)

## 📜 Licencia
Este proyecto está bajo la Licencia MIT. Consulta el archivo [LICENSE](LICENSE) para más detalles.
