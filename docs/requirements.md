# Requisitos funcionales

Este documento define el comportamiento esperado de la API de inventario usada
en la demostración de adecuación funcional de VERAUD.

## REQ-01: Listar productos

La API debe devolver todos los productos registrados en el inventario.

- `GET /products` responde con código `200`.
- La respuesta es una lista de productos.
- Si no existen productos, la respuesta es una lista vacía.

## REQ-02: Consultar productos por ID

La API debe permitir consultar un producto concreto mediante su identificador.

- `GET /products/{product_id}` responde con el producto solicitado.
- El producto incluye `id`, `name`, `price`, `stock` y `ratings`.
- Si el producto no existe, se debe informar un error `404`.

## REQ-03: Crear productos con validación

La API debe crear productos válidos y rechazar datos inválidos.

- `POST /products` responde con código `201` cuando el producto es válido.
- El nombre no puede estar vacío ni contener solo espacios.
- El precio no puede ser negativo.
- El stock inicial no puede ser negativo.
- Las valoraciones deben ser numéricas y estar entre `0` y `5`.
- Una solicitud inválida responde con código `422`.

## REQ-04: Actualizar stock sin valores negativos

La API debe actualizar el stock de un producto existente.

- `PATCH /products/{product_id}/stock` actualiza el valor de `stock`.
- Se permite el valor límite `0`.
- Un stock negativo debe rechazarse con código `422`.
- Un producto inexistente debe informar un error `404`.

## REQ-05: Eliminar productos

La API debe eliminar un producto existente del inventario.

- `DELETE /products/{product_id}` responde con código `204`.
- Después de eliminar el producto, este ya no debe aparecer en el listado.
- El producto tampoco debe poder recuperarse del repositorio.

## REQ-06: Calcular el promedio de valoraciones

La API debe calcular la media aritmética de las valoraciones de un producto.

- `GET /products/{product_id}/average-rating` devuelve el promedio.
- Para las valoraciones `[4.0, 5.0]`, el promedio esperado es `4.5`.
- Si el producto no existe, se debe informar un error `404`.

## REQ-07: Calcular correctamente el total de una compra

La API debe calcular el importe total de una compra.

- `POST /purchases/total` recibe una lista de líneas de compra.
- Cada línea contiene `product_id` y `quantity`.
- El total se calcula como la suma de `precio_unitario * cantidad`.
- Una compra vacía tiene un total de `0.0`.
- Una cantidad menor o igual que cero es inválida y responde con `422`.
- Un producto inexistente responde con `404`.

Ejemplo: dos unidades de un producto de `50.0` y tres unidades de un producto
de `20.0` dan un total de `160.0`.

## REQ-08: Validar contraseñas de mínimo ocho caracteres

El sistema debe validar la longitud mínima de una contraseña.

- `POST /passwords/validate` devuelve `{"valid": true}` si la contraseña tiene
  al menos ocho caracteres.
- Una contraseña de siete caracteres o menos devuelve `{"valid": false}`.
- Una contraseña de exactamente ocho caracteres es válida.
- Un valor que no sea una cadena devuelve `{"valid": false}`.
