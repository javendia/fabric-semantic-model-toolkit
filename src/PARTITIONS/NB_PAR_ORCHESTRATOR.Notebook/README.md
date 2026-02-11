# NB_PAR_ORCHESTRATOR

[![Python](https://img.shields.io/badge/Python-3.10+-blue.svg)](https://www.python.org/)

## 📋 Resumen

El cuaderno **NB_PAR_ORCHESTRATOR** es el orquestador principal del flujo de trabajo para la gestión de particiones y refresco de datos en conjuntos de datos de Power BI dentro de Microsoft Fabric. Este cuaderno coordina la creación automática de particiones y la actualización selectiva de tablas o particiones según las configuraciones definidas por el usuario.

---

## ➡️ Parámetros de entrada

### Configuración básica

| Parámetro | Tipo | Descripción | Ejemplo |
|-----------|------|-------------|---------|
| `workspace_id` | string | GUID del área de trabajo de Microsoft Fabric | `"dc1b17ac-1d39-4be3-a848-45c8a55c05f1"` |
| `dataset_id` | string | GUID del modelo semántico de Power BI | `"0e4e85ca-f446-44b6-bf18-2a9114668242"` |

### Parámetros globales
| Parámetro | Tipo | Descripción | Ejemplo |
|-----------|------|-------------|---------|
| `partitions_config` | string (JSON) | Configuración para la creación y el refresco de particiones | Ver tabla abajo |

**Ejemplo de `partitions_config`:**
```json
[
  {
    "table": "Sales",
    "first_date": "20200101",
    "partition_by": "Order Date",
    "interval": "QUARTER",
    "last_date": "20250101",
    "intervals_to_refresh": "*"
  }
]
```

| Campo | Tipo | Descripción | Ejemplo |
|-------|------|-------------|---------|
| `table` | string | Nombre de la entidad del modelo semántico a particionar | `"Sales"` |
| `first_date` | string | Fecha inicial de particionamiento (formato YYYYMMDD) | `"20200101"` |
| `partition_by` | string | Nombre de la columna de fecha para particionar | `"Order Date"` |
| `interval` | string | Intervalo de particionamiento | `"MONTH"`, `"QUARTER"`, `"YEAR"` |
| `last_date` | string | Fecha final de particionamiento o partir de la cual refrescar (formato YYYYMMDD) | `"20250101"` |
| `intervals_to_refresh` | string | Cuántos períodos incluir. Si el valor es *, refresca todos los períodos disponibles | `"4"` |

### Parámetros de particionamiento

| Parámetro | Tipo | Descripción | Ejemplo |
|-----------|------|-------------|---------|
| `enable_partition` | boolean | Habilita/deshabilita la creación de particiones | `True` / `False` |

### Parámetros de refresco

| Parámetro | Tipo | Descripción | Ejemplo |
|-----------|------|-------------|---------|
| `enable_refresh` | boolean | Habilita/deshabilita el refresco del modelo semántico | `True` / `False` |
| `tables_to_refresh` | string | Tablas a refrescar (separadas por comas) | `"Customer,Sales"` |
| `partitions_to_refresh` | string (JSON) | Particiones específicas a refrescar | Ver tabla abajo |

**Ejemplo de `partitions_to_refresh`:**
```json
[
  {
    "table": "Sales",
    "selected_partitions": "Sales_20200101_20200331,Sales_20200401_20200630"
  }
]
```

### Parámetros de ejecución

| Parámetro | Tipo | Descripción | Valores |
|-----------|------|-------------|---------|
| `refresh_commit_mode` | string | Confirmación de transacciones | `"transactional"` (predeterminado) o `"partialBatch"` |
| `refresh_max_parallelism` | integer | Número máximo de entidades a refrescar en paralelo | (recomendado: `4-6`) |
| `notebook_timeout` | integer | Tiempo máximo de ejecución del cuaderno en segundos | (recomendado: `7200`) |

---

## 🔄 Flujo de acciones

```mermaid
flowchart TD
  A["🟢 INICIO<br/>Validación de parámetros"] --> B{¿enable_partition<br/>activo?}
  B -->|Sí| C["📌 Ejecutar NB_PAR_PARTITIONER<br/>(Crear particiones)"]
  B -->|No| D["⏭️ Particionamiento deshabilitado"]
  C --> E{¿Particionamiento<br/>con éxito?}
  C -->|No| X["❌ Error crítico<br/>Abortar ejecución"]
  C -->|Sí| F{¿enable_refresh<br/>activo?}
  D --> F
  F -->|No| Z["✅ FIN<br/>"]
  F -->|Sí| G{¿partitions_to_refresh<br/>proporcionado?}
  G -->|Sí| H["📋 Usar partitions_to_refresh<br/>explícito"]
  G -->|No| I{¿partitions_config<br/>proporcionado?}
  I -->|Sí| J["📊 Generar lista de particiones<br/>generate_partitions_list()"]
  I -->|No| K["🔄 Refrescar todas<br/>las particiones"]
  J --> L{¿Generación<br/>con éxito?}
  L -->|No| X
  L -->|Sí| H
  H --> N["🔄 Ejecutar NB_PAR_REFRESHER<br/>(Refrescar modelo)"]
  K --> N
  N --> O{¿Refresco<br/>con éxito?}
  O -->|No| X
  O -->|Sí| Z
  X --> END["⛔ Fin con error"]
  Z --> END2["✅ Fin con éxito"]
  style A fill:#90EE90,color:#000
  style Z fill:#87CEEB,color:#000
  style END2 fill:#87CEEB,color:#000
  style X fill:#FFB6C6,color:#000
  style END fill:#FFB6C6,color:#000
  style C fill:#FFE4B5,color:#000
  style N fill:#FFE4B5,color:#000
```

---

## 📦 Dependencias

### Bibliotecas externas

- **pandas**: Manipulación de DataFrames.
- **datetime**: Cálculos de fechas.
- **typing**: Tipos (Optional, Any, Dict).
- **logging**: Sistema de logging.
- **notebookutils**: Paquete integrado para llevar a cabo tareas comunes en cuadernos de Microsoft Fabric.
- **StringIO**: Manejo de strings como archivos.
- **uuid**: Generación de identificadores únicos.
- **numpy**: Operaciones numéricas y manejo de arrays.

### fabtoolkit

Conjunto de utilidades personalizadas para facilitar operaciones comunes en Microsoft Fabric.

```python
from fabtoolkit.utils import (
    get_bounds_from_offset,       # Calcular fechas límite
    generate_date_ranges,         # Generar intervalos de fechas
    is_valid_text,                # Validar texto no vacío
    validate_json,                # Analizar y validar JSON
    Constants
)
from fabtoolkit.log import ConsoleFormatter    # Formato de logging personalizado
```

**Versión de fabtoolkit:** `1.0.0`

---

## 📈 Ejemplo de ejecución

### 1. Solo particionar hasta la fecha actual
```python
enable_partition = True
partitions_config = '[{"table": "Sales", "first_date": "20200101", "partition_by": "Order Date", "interval": "QUARTER", "last_date": "TODAY", "intervals_to_refresh": "*"}]'
enable_refresh = False
```

### 2. Particionar hasta una determinada fecha y refrescar todos los períodos
```python
enable_partition = True
partitions_config = '[{"table": "Sales", "first_date": "20200101", "partition_by": "Order Date", "interval": "QUARTER", "last_date": "20250101", "intervals_to_refresh": "*"}]'
enable_refresh = True
tables_to_refresh = ""
partitions_to_refresh = ""
refresh_commit_mode = "transactional"
refresh_max_parallelism = 6
notebook_timeout = 7200
```

### 3. Solo refrescar algunas tablas y un rango de particiones específico
```python
enable_partition = False
partitions_config = '[{"table": "Sales", "first_date": "20200101", "partition_by": "Order Date", "interval": "QUARTER", "last_date": "20250101", "intervals_to_refresh": "4"}]'
enable_refresh = True
tables_to_refresh = "Customer,Sales"
partitions_to_refresh = ""
refresh_commit_mode = "transactional"
refresh_max_parallelism = 6
notebook_timeout = 7200
```

### 4. Solo refrescar particiones específicas
```python
enable_partition = False
partitions_config = '[{"table": "Sales", "first_date": "20200101", "partition_by": "Order Date", "interval": "QUARTER", "last_date": "20250101", "intervals_to_refresh": "*"}]'
enable_refresh = True
tables_to_refresh = ""
partitions_to_refresh = '[{"table": "Sales", "selected_partitions": "Sales_20200101_20200331,Sales_20200401_20200630"}]'
refresh_commit_mode = "transactional"
refresh_max_parallelism = 4
notebook_timeout = 7200
```

---

## 🔗 Cuadernos relacionados

- [**NB_PAR_PARTITIONER**](./NB_PAR_PARTITIONER.Notebook/README.md): Genera particiones dinámicamente en función de criterios de fecha personalizables.
- [**NB_PAR_REFRESHER**](./NB_PAR_REFRESHER.Notebook/README.md): Ejecuta el refresco del conjunto de datos para un grupo de tablas / particiones especificadas.

---