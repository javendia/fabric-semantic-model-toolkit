# NB_PAR_PARTITIONER

[![Python](https://img.shields.io/badge/Python-3.10+-blue.svg)](https://www.python.org/)

## 📋 Resumen

El cuaderno **NB_PAR_PARTITIONER** es responsable de la **creación de particiones en modelos semánticos de Power BI**. Valida la configuración de particionamiento proporcionada por el usuario, genera automáticamente los intervalos de fechas necesarios y crea las particiones en el modelo semántico especificado.

---

## ➡️ Parámetros de entrada

| Parámetro | Tipo | Descripción | Ejemplo |
|-----------|------|-------------|---------|
| `workspace_id` | string | GUID del área de trabajo de Microsoft Fabric. | `"dc1b17ac-1d39-4be3-a848-45c8a55c05f1"` |
| `dataset_id` | string | GUID del modelo semántico de Power BI.| `"0e4e85ca-f446-44b6-bf18-2a9114668242"` |
| `partitions_config` | string (JSON) | Configuración de particiones a crear. | Ver tabla abajo |

**Ejemplo de `partitions_config`:**
```json
[
  {
    "table": "Sales",
    "first_date": "20200101",
    "partition_by": "Order Date",
    "interval": "QUARTER",
    "last_date": "20250101"
  }
]
```

| Campo | Tipo | Descripción | Ejemplo |
|-------|------|-------------|---------|
| `table` | string | Nombre de la entidad del modelo semántico a particionar | `"Sales"` |
| `first_date` | string | Fecha inicial de particionamiento (formato YYYYMMDD) | `"20200101"` |
| `partition_by` | string | Nombre de la columna de fecha para particionar | `"Order Date"` |
| `interval` | string | Intervalo de particionamiento | `MONTH`, `QUARTER`, `YEAR` |
| `last_date` | string | Fecha final de particionamiento (formato YYYYMMDD) | `"20250101"` |

El cuaderno valida automáticamente:
- ✅ Que todas las entidades en `partitions_config` existan en el modelo semántico.
- ✅ Que todas las columnas `partition_by` sean válidas.
- ✅ Que `first_date` esté en formato YYYYMMDD.
- ✅ Que `last_date` esté en formato YYYYMMDD.
- ✅ Que `interval` sea un valor válido (`MONTH`, `QUARTER` o `YEAR`).

---

## 🔄 Flujo de acciones

```mermaid
flowchart TD
    A["🟢 INICIO<br/>partition()"] --> B["📊 Crear instancia Dataset<br/>Obtener el nombre del área de trabajo, el nombre del modelo semántico y las particiones existentes"]
    
    B --> C["✅ Validar configuración"]
    
    C --> D{¿Validación<br/>con éxito?}
    D -->|No| X["❌ Error validación<br/>Mostrar detalles<br/>Abortar"]
    D -->|Sí| E["🔄 Para cada tabla<br/>en la configuración"]
    
    E --> F["📋 Generar intervalos de fechas"]
    
    F --> G["📝 Crear nombres de particiones<br/>Formato: table_YYYYMMDD_YYYYMMDD<br/>Ej: Sales_20200101_20200331"]
    
    G --> H["🔍 Comparar con las existentes<br/>¿La partición ya existe?"]
    
    H -->|Sí| I["⏭️ La partición existe<br/>No requiere creación"]
    H -->|No| J["⚡ Pendiente de crear"]
    
    I --> K{¿Hay particiones<br/>pendientes de crear?}
    J --> K
    
    K -->|No| L["ℹ️ Todas las particiones<br/>ya existen"]
    K -->|Sí| M["Extraer la consulta original<br/>Obtener último paso"]
    
    M --> N["🔧 Generar consultas M"]
    
    N --> O["💾 Crear particiones"]
    
    O --> P{¿Creación<br/>con éxito?}
    P -->|No| X
    P -->|Sí| Q["✅ Particiones creadas"]
    
    Q --> R{¿Existe la partición<br/>por defecto?<br/>tabla == partition_name}
    
    R -->|Sí| S["🗑️ Eliminar partición por defecto"]
    R -->|No| T["ℹ️ Sin partición<br/>por defecto"]
    
    S --> U{¿Más entidades?}
    T --> U
    L --> U
    
    U -->|Sí| E
    U -->|No| V["✅ FIN <br/>Se han procesado todas las entidades del listado de configuración"]
    
    V --> END["✅ Fin con éxito"]
    X --> END2["⛔ Fin con error"]
    
    style A fill:#90EE90,color:#000
    style V fill:#87CEEB,color:#000
    style END fill:#87CEEB,color:#000
    style X fill:#FFB6C6,color:#000
    style END2 fill:#FFB6C6,color:#000
    style C fill:#FFE4B5,color:#000
    style F fill:#FFE4B5,color:#000
    style O fill:#FFE4B5,color:#000
```

---

## 📦 Dependencias

### Bibliotecas externas

- **pandas**: Manipulación de DataFrames.
- **datetime**: Cálculos de fechas.
- **typing**: Tipos (Dict, List).
- **logging**: Sistema de logging.
- **sys**: Manejo de excepciones y salida del programa.
- **StringIO**: Manejo de strings como archivos.

### fabtoolkit

Conjunto de utilidades personalizadas para facilitar operaciones comunes en Microsoft Fabric.

```python
from fabtoolkit.utils import (
    generate_date_ranges,     # Generar intervalos de fechas
    Constants,                # Constantes globales (DATE_FORMAT, INTERVALS)
    Interval                  # Enum de intervalos válidos
)
from fabtoolkit.log import ConsoleFormatter    # Formato de logging personalizado
from fabtoolkit.dataset import Dataset         # Clase para operaciones sobre modelos semánticos
```

**Versión de fabtoolkit:** `1.0.0`

---

## Ejemplos de uso

### Ejemplo 1: Particionar una tabla por trimestre

```json
[
  {
    "table": "Sales",
    "first_date": "20200101",
    "partition_by": "Order Date",
    "interval": "QUARTER",
    "last_date": "20250101"
  }
]
```

**Resultado esperado (a 27/12/2025):**
```
Sales_20200101_20200331  (Q1 2020)
Sales_20200401_20200630  (Q2 2020)
Sales_20200701_20200930  (Q3 2020)
... (continúa hasta Q4 2025)
Sales_20251001_20251231  (Q4 2025)
```

### Ejemplo 2: Múltiples entidades con diferentes intervalos

```json
[
  {
    "table": "Sales",
    "first_date": "20200101",
    "partition_by": "Delivery Date",
    "interval": "QUARTER",
    "last_date": "20250101"
  },
  {
    "table": "Orders",
    "first_date": "20250101",
    "partition_by": "Order Date",
    "interval": "MONTH",
    "last_date": "20251231"
  }
]
```

---

## 📝 Notas de implementación

### Generación de intervalo de fechas

- El intervalo se calcula hasta el **último día del período para el valor de `last_date`**:
  - Si el intervalo es `YEAR`: hasta el final del año para el valor de `last_date`.
  - Si el intervalo es `QUARTER`: hasta el final del trimestre para el valor de `last_date`.
  - Si el intervalo es `MONTH`: hasta el final del mes para el valor de `last_date`.

### Eliminación de partición por defecto

- Generalmente, por defecto, Power BI crea una partición que abarca todos los datos, cuyo nombre coincide con la entidad.
- Una vez añadidas las particiones necesarias, esta partición se elimina en caso de que exista.

### Construcción de consultas M para particiones

- Se preserva la consulta original (transformaciones, uniones, etc.)
- Se agrega un paso adicional `Table.SelectRows` para filtrar por un intervalo de fechas específico.

---