# NB_PAR_REFRESHER

[![Python](https://img.shields.io/badge/Python-3.10+-blue.svg)](https://www.python.org/)

## 📋 Resumen

El cuaderno **NB_PAR_REFRESHER** es responsable de la **ejecución controlada de refrescos de datos en modelos semánticos de Power BI**. Permite a los usuarios especificar entidades y particiones concretas para refrescar, optimizando así el uso de recursos y reduciendo los tiempos de actualización al evitar refrescos completos innecesarios.

---

## ➡️ Parámetros de entrada

### Configuración básica

| Parámetro | Tipo | Descripción | Ejemplo |
|-----------|------|-------------|---------|
| `workspace_id` | string | GUID del área de trabajo de Microsoft Fabric | `"dc1b17ac-1d39-4be3-a848-45c8a55c05f1"` |
| `dataset_id` | string | GUID del modelo semántico de Power BI | `"0e4e85ca-f446-44b6-bf18-2a9114668242"` |

### Parámetros de refresco

| Parámetro | Tipo | Descripción | Ejemplo | Por defecto |
|-----------|------|-------------|---------|-------------|
| `tables_to_refresh` | string | Entidades a refrescar (separadas por comas) | `"Customer,Sales"` | Todas las entidades |
| `partitions_to_refresh` | string (JSON) | Particiones específicas a refrescar | Ver tabla abajo | Todas las particiones |
| `commit_mode` | string | Confirmación de transacciones | `"transactional"`, `"partialBatch"` | `"transactional"` |
| `max_parallelism` | integer | Número máximo de entidades a refrescar en paralelo | `6` | `4` |

#### `tables_to_refresh`

- **Formato:** Cadena con nombres de entidades separados por comas.

  ```plaintext
  "Customer,Product,Sales"
  ```

- **Comportamiento:**
  - Si se proporcionan tablas existentes en el modelo semántico, refresca solo dichas entidades junto a sus dependencias. 
    - En caso de que alguna entidad no exista, se omite y se muestra una advertencia.
    - Si todas las entidades proporcionadas son inválidas, se muestra un error y se aborta el proceso.
  - Si está vacío, refresca todas las entidades del modelo semántico.

#### `partitions_to_refresh`

- **Formato:** JSON de entidades y particiones a refrescar 

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

- **Comportamiento:**
  - Si se proporciona un valor válido, refresca solo las particiones especificadas.
    - Si una entidad aparece en el parámetro `tables_to_refresh` pero no en `partitions_to_refresh`, se refrescan todas sus particiones.
    - Si una entidad aparece en el parámetro `partitions_to_refresh`, se refrescan solo las particiones listadas.
  - Si está vacío, refresca todas las particiones de las entidades seleccionadas.
  - En caso de que alguna tabla o partición no existan, se omite y se muestra una advertencia.
---

## 🔄 Flujo de acciones

```mermaid
flowchart TD
  A["🟢 INICIO<br/>refresh()"] --> B["📊 Crear instancia Dataset<br/>Obtener nombres y metadatos"]
  B --> C["📋 Identificar tablas a refrescar"]
  C --> D{¿tables_to_refresh proporcionado?}
  D -->|No| E["Obtener todas las tablas disponibles"]
  D -->|Sí| F["Separar por comas y limpiar"]
  F --> G["Validar contra el modelo semántico"]
  G --> H{¿Tablas inválidas?}
  H -->|Sí| I["⚠️ Advertencia: Existen tablas inválidas<br/>Omitir inválidas"]
  I --> J{¿Quedan tablas válidas?}
  J -->|No| X["❌ Error: todas inválidas<br/>Abortar"]
  J -->|Sí| K["Obtener tablas relacionadas"]
  H -->|No| K
  E --> L["Obtener tablas relacionadas"]
  K --> M["✅ Tablas a refrescar"]
  L --> M
  M --> N["📋 Identificar particiones a refrescar"]
  N --> O{¿partitions_to_refresh proporcionado?}
  O -->|No| P["Obtener todas las particiones del resto de las tablas seleccionadas"]
  O -->|Sí| Q["Leer y parsear JSON de particiones"]
  Q --> R["Validar si las tablas con particiones seleccionadas existen entre las tablas seleccionadas"]
  R --> S{¿Tablas de particiones no seleccionadas?}
  S -->|Sí| T["⚠️ Advertencia: Existen tablas inválidas con particiones seleccionadas<br/>Omitir"]
  T --> U{¿Quedan tablas válidas?}
  U -->|No| P
  U -->|Sí| V["Validar particiones por tabla"]
  S -->|No| V
  V --> W{¿Particiones inválidas?}
  W -->|Sí| X1["⚠️ Advertencia: Particiones inválidas<br/>Omitir"]
  X1 --> Y["Componer listado de particiones"]
  W -->|No| Y
  Y --> Z["✅ Particiones a refrescar"]
  P --> Z
  Z --> AA["📤 Solicitar refresco"]
  AA --> AB["🔄 Obtener identificador del refresco"]
  AB --> AC{¿GUID válido?}
  AC -->|No| X["⛔ Fin con error"]
  AC -->|Sí| AD["⏳ Monitorear estado"]
  AD --> AE{¿Estado final?}
  AE -->|Completed| END2["✅ Refresco completado"]
  AE -->|Failed| X["❌ Refresco fallido"]
  END2 --> END3["✅ Fin con éxito"]
  style A fill:#90EE90,color:#000
  style END2 fill:#87CEEB,color:#000
  style END3 fill:#87CEEB,color:#000
  style X fill:#FFB6C6,color:#000
  style X1 fill:#FFD580,color:#000
  style I fill:#FFD580,color:#000
  style T fill:#FFD580,color:#000
  style END fill:#FFB6C6,color:#000
  style AA fill:#FFE4B5,color:#000
  style AD fill:#FFE4B5,color:#000
```

---

### Bibliotecas externas

- **pandas**: Manipulación de DataFrames.
- **logging**: Sistema de logging.
- **sys**: Manejo de excepciones y salida del programa.
- **typing**: Tipos (List, Optional).
- **StringIO**: Manejo de strings como archivos.

### fabtoolkit

Conjunto de utilidades personalizadas para facilitar operaciones comunes en Microsoft Fabric.

```python
from fabtoolkit.utils import (
    is_valid_text          # Validar string no vacío
)
from fabtoolkit.log import ConsoleFormatter    # Formato de logging personalizado
from fabtoolkit.dataset import Dataset         # Clase para operaciones sobre modelos semánticos
```

---

## Ejemplos de uso

### Ejemplo 1: Refrescar todas las entidades y particiones

```python
tables_to_refresh = None
partitions_to_refresh = None
commit_mode = "transactional"
max_parallelism = 4
```

### Ejemplo 2: Refrescar solo una entidad y todas sus particiones

```python
tables_to_refresh = "Sales"
partitions_to_refresh = None
commit_mode = "transactional"
max_parallelism = 4
```

### Ejemplo 3: Refrescar solo una entidad y particiones específicas

```python
tables_to_refresh = "Sales"
partitions_to_refresh = '[
  {
    "table": "Sales",
    "selected_partitions": ["Sales_20250101_20250331", "Sales_20250401_20250630"]
  }
]'
commit_mode = "transactional"
max_parallelism = 4
```

---

## 📝 Notas de implementación

### Búsqueda de entidades relacionadas
```python
dataset.get_related_tables(["Sales"])
# Devuelve: [Sales, Customer, Product, Store, etc.]
# Todas las entidades con relaciones directas/indirectas
```

---