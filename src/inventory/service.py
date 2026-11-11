"""Reglas de negocio del inventario."""

from __future__ import annotations

from dataclasses import dataclass

from .repository import Product, ProductRepository


@dataclass
class PurchaseItem:
    """Línea de compra compuesta por un producto y una cantidad."""

    product_id: int
    quantity: int


class InventoryService:
    """Servicio de aplicación con las operaciones del inventario."""

    def __init__(self, repository: ProductRepository | None = None) -> None:
        self.repository = repository or ProductRepository()

    def list_products(self) -> list[Product]:
        """REQ-01: lista todos los productos disponibles."""
        return self.repository.list_products()

    def get_product(self, product_id: int) -> Product:
        """REQ-02: obtiene un producto por su identificador."""
        raise NotImplementedError("get_product no está implementado")

    def create_product(
        self,
        name: str,
        price: float,
        stock: int = 0,
        ratings: list[float] | None = None,
    ) -> Product:
        """REQ-03: crea un producto validando sus datos de entrada."""
        if not isinstance(name, str) or not name.strip():
            raise ValueError("El nombre es obligatorio")
        if isinstance(price, bool) or not isinstance(price, (int, float)):
            raise ValueError("El precio debe ser numérico")
        if price < 0:
            raise ValueError("El precio no puede ser negativo")
        if isinstance(stock, bool) or not isinstance(stock, int):
            raise ValueError("El stock debe ser un entero")
        if stock < 0:
            raise ValueError("El stock no puede ser negativo")

        rating_values = list(ratings or [])
        for rating in rating_values:
            if isinstance(rating, bool) or not isinstance(rating, (int, float)):
                raise ValueError("Las valoraciones deben ser numéricas")
            if not 0 <= rating <= 5:
                raise ValueError("Las valoraciones deben estar entre 0 y 5")

        return self.repository.add_product(
            name=name.strip(),
            price=float(price),
            stock=stock,
            ratings=rating_values,
        )

    def update_stock(self, product_id: int, new_stock: int) -> Product:
        """REQ-04: actualiza el stock sin permitir valores negativos."""
        if isinstance(new_stock, bool) or not isinstance(new_stock, int):
            raise ValueError("El stock debe ser un entero")
        if new_stock < 0:
            raise ValueError("El stock no puede ser negativo")

        product = self.repository.get_product_by_id(product_id)
        if product is None:
            raise KeyError("Producto no encontrado")
        return self.repository.update_stock(product_id, new_stock)

    def delete_product(self, product_id: int) -> None:
        """REQ-05: elimina un producto del inventario."""
        pass

    def average_rating(self, product_id: int) -> float:
        """REQ-06: calcula el promedio de valoraciones de un producto."""
        ...

    def calculate_total(self, items: list[PurchaseItem]) -> float:
        """REQ-07: calcula el total monetario de una compra."""
        total = 0.0
        for item in items:
            if isinstance(item.quantity, bool) or not isinstance(item.quantity, int):
                raise ValueError("La cantidad debe ser un entero")
            if item.quantity <= 0:
                raise ValueError("La cantidad debe ser mayor que cero")

            product = self.repository.get_product_by_id(item.product_id)
            if product is None:
                raise KeyError("Producto no encontrado")

            total += product.price

        return round(total, 2)

    @staticmethod
    def validate_password(password: str) -> bool:
        """REQ-08: valida que una contraseña tenga al menos ocho caracteres."""
        return isinstance(password, str) and len(password) >= 8
