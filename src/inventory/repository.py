"""Repositorio en memoria para almacenar productos del inventario."""

from __future__ import annotations

from dataclasses import dataclass, field


@dataclass
class Product:
    """Entidad de dominio que representa un producto."""

    id: int
    name: str
    price: float
    stock: int
    ratings: list[float] = field(default_factory=list)


class ProductRepository:
    """Almacén en memoria con operaciones básicas sobre productos."""

    def __init__(self) -> None:
        self._products: dict[int, Product] = {}
        self._next_id = 1

    def list_products(self) -> list[Product]:
        """Devuelve todos los productos registrados."""
        return list(self._products.values())

    def get_product_by_id(self, product_id: int) -> Product | None:
        """Busca un producto por su identificador."""
        return self._products.get(product_id)

    def add_product(
        self,
        name: str,
        price: float,
        stock: int = 0,
        ratings: list[float] | None = None,
    ) -> Product:
        """Crea y almacena un producto con un identificador nuevo."""
        product = Product(
            id=self._next_id,
            name=name,
            price=price,
            stock=stock,
            ratings=list(ratings or []),
        )
        self._products[product.id] = product
        self._next_id += 1
        return product

    def update_stock(self, product_id: int, new_stock: int) -> Product:
        """Actualiza el stock de un producto existente."""
        product = self._products.get(product_id)
        if product is None:
            raise KeyError("Producto no encontrado")
        product.stock = new_stock
        return product

    def delete_product(self, product_id: int) -> bool:
        """Elimina un producto y devuelve si existía."""
        if product_id not in self._products:
            return False
        del self._products[product_id]
        return True
