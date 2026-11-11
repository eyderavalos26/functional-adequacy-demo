# Resultado esperado de la auditoría

Este proyecto contiene cuatro defectos intencionales para comprobar la
capacidad de detección de VERAUD. Los defectos no deben corregirse dentro de
esta demostración.

## Defectos intencionales

### DEF-01: `get_product` no implementado

- **Requisito afectado:** REQ-02.
- **Ubicación:** `src/inventory/service.py`, método `InventoryService.get_product`.
- **Comportamiento:** lanza `NotImplementedError` en lugar de devolver el
  producto solicitado.
- **Prueba que debe fallar:** `test_req02_get_product_by_id_expected_failure`.

### DEF-02: `delete_product` no elimina el producto

- **Requisito afectado:** REQ-05.
- **Ubicación:** `src/inventory/service.py`, método `InventoryService.delete_product`.
- **Comportamiento:** el método contiene únicamente `pass`, por lo que la
  operación finaliza sin eliminar nada.
- **Prueba que debe fallar:** `test_req05_delete_product_expected_failure`.

### DEF-03: `average_rating` no calcula el promedio

- **Requisito afectado:** REQ-06.
- **Ubicación:** `src/inventory/service.py`, método `InventoryService.average_rating`.
- **Comportamiento:** el cuerpo del método es `...`, por lo que devuelve
  `None` en lugar del promedio.
- **Prueba que debe fallar:** `test_req06_average_rating_expected_failure`.

### DEF-04: `calculate_total` ignora la cantidad

- **Requisito afectado:** REQ-07.
- **Ubicación:** `src/inventory/service.py`, método `InventoryService.calculate_total`.
- **Comportamiento:** suma únicamente el precio unitario de cada línea y no lo
  multiplica por la cantidad. No existen marcadores de stub en este defecto.
- **Pruebas que deben fallar:**
  - `test_req07_calculate_total_multiple_quantities_expected_failure`.
  - `test_req07_calculate_total_api_expected_failure`.

## Requisitos que deben pasar

- REQ-01: listado de productos.
- REQ-03: creación y validación de productos.
- REQ-04: actualización de stock y rechazo de valores negativos.
- REQ-08: validación de contraseñas de mínimo ocho caracteres.

Las pruebas de estos requisitos deben finalizar correctamente. El resto de
pruebas de REQ-07 (compra vacía, cantidad cero y una sola unidad) también deben
pasar, porque el defecto se manifiesta al usar cantidades mayores que uno o
varias líneas de compra.

## Resultado global esperado

Ejecutando `uv run pytest -q` se esperan exactamente cinco fallos, todos
asociados a los cuatro defectos intencionales. Cualquier otro fallo indicaría
un problema de configuración o una regresión no intencional.
