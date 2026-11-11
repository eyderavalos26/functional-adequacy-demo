# VERAUD - Demostración de Adecuación Funcional

API de inventario construida con Python y FastAPI para demostrar la detección
de defectos funcionales por parte de VERAUD.

El proyecto contiene ocho requisitos funcionales. Cuatro de ellos incluyen
defectos intencionales que **no deben corregirse** dentro de esta demostración.
El resto de la funcionalidad está implementada correctamente y cuenta con
pruebas positivas, negativas y de límites.

## Estructura

```text
functional-adequacy-demo/
├── README.md
├── pyproject.toml
├── docs/
│   ├── requirements.md
│   └── expected-audit.md
├── src/
│   └── inventory/
│       ├── __init__.py
│       ├── api.py
│       ├── repository.py
│       └── service.py
├── tests/
│   └── test_inventory.py
└── ground_truth/
    ├── requirements.json
    └── expected_findings.json
```

## Requisitos

| ID | Funcionalidad | Estado |
| --- | --- | --- |
| REQ-01 | Listar productos | Implementado |
| REQ-02 | Consultar producto por ID | Defecto intencional |
| REQ-03 | Crear productos con validación | Implementado |
| REQ-04 | Actualizar stock sin valores negativos | Implementado |
| REQ-05 | Eliminar productos | Defecto intencional |
| REQ-06 | Promedio de valoraciones | Defecto intencional |
| REQ-07 | Total de una compra | Defecto intencional |
| REQ-08 | Contraseñas de mínimo ocho caracteres | Implementado |

La especificación completa está en `docs/requirements.md`.

## Defectos intencionales

1. `InventoryService.get_product` lanza `NotImplementedError`.
2. `InventoryService.delete_product` contiene únicamente `pass`.
3. `InventoryService.average_rating` contiene únicamente `...`.
4. `InventoryService.calculate_total` suma el precio unitario sin multiplicarlo
   por la cantidad; no tiene marcadores de stub.

El detalle de los hallazgos esperados y de las pruebas que deben fallar está en
`docs/expected-audit.md` y en `ground_truth/expected_findings.json`.

## Instalación

Se requiere `uv`:

```bash
uv sync --dev
```

## Ejecución de las pruebas

```bash
uv run pytest -q
```

Resultado esperado: las pruebas de REQ-01, REQ-03, REQ-04 y REQ-08 pasan. Las
pruebas asociadas a los cuatro defectos fallan de forma intencional. En total se
esperan cinco fallos:

- `test_req02_get_product_by_id_expected_failure` (DEF-01).
- `test_req05_delete_product_expected_failure` (DEF-02).
- `test_req06_average_rating_expected_failure` (DEF-03).
- `test_req07_calculate_total_multiple_quantities_expected_failure` (DEF-04).
- `test_req07_calculate_total_api_expected_failure` (DEF-04).

Cualquier otro fallo indicaría un problema de configuración o una regresión no
intencional.

## Ejecución de la API

```bash
uv run uvicorn inventory.api:app --reload
```

La documentación interactiva de FastAPI queda disponible en
`http://127.0.0.1:8000/docs`.

## Endpoints

| Método | Ruta | Requisito |
| --- | --- | --- |
| GET | `/products` | REQ-01 |
| GET | `/products/{product_id}` | REQ-02 |
| POST | `/products` | REQ-03 |
| PATCH | `/products/{product_id}/stock` | REQ-04 |
| DELETE | `/products/{product_id}` | REQ-05 |
| GET | `/products/{product_id}/average-rating` | REQ-06 |
| POST | `/purchases/total` | REQ-07 |
| POST | `/passwords/validate` | REQ-08 |

## Notas

- El código fuente está en inglés.
- Los comentarios, docstrings y documentación están en español.
- No se utilizan servicios de IA ni APIs externas.
- Los datos se almacenan en memoria y se pierden al reiniciar el proceso.



## Auditoría reproducible con VERAUD — EP-004

Esta demostración está diseñada para evaluar el agente de Adecuación Funcional de VERAUD mediante análisis exploratorio de repositorios.

### Requisitos

- Git.
- uv.
- Python 3.11 o 3.12 para la demostración.
- Python 3.13 o superior para VERAUD.

### 1. Obtener los repositorios

```bash
mkdir -p ~/veraud-demo-workspace
cd ~/veraud-demo-workspace

git clone --branch feat/functional-adequacy-ep004-delivery \
  https://github.com/redsquirrelx/veraud.git

git clone https://github.com/redsquirrelx/functional-adequacy-demo.git
```

### 2. Ejecutar las pruebas del proyecto de demostración

```bash
cd ~/veraud-demo-workspace/functional-adequacy-demo
uv sync --dev
uv run pytest -q
```

Se esperan cinco fallos intencionales correspondientes a los defectos documentados.

### 3. Instalar VERAUD

```bash
cd ~/veraud-demo-workspace/veraud/agent-server
uv sync
```

### 4. Ejecutar el agente de Adecuación Funcional

```bash
uv run functional-adequacy \
  --repository ~/veraud-demo-workspace/functional-adequacy-demo \
  --output /tmp/functional_adequacy_demo_result.json
```

La auditoría exploratoria no requiere credenciales de proveedores LLM.

### 5. Consultar los resultados

El resultado se genera en:

`/tmp/functional_adequacy_demo_result.json`

Puede visualizarse mediante:

```bash
python -m json.tool /tmp/functional_adequacy_demo_result.json
```

### Resultados de referencia

En la ejecución del 10 de noviembre de 2026 se obtuvieron:

- 34 capacidades detectadas.
- 102 hallazgos generados.

Estos valores corresponden a la versión de referencia y pueden variar ante cambios en el código o en el agente.
