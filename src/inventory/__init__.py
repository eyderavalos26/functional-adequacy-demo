"""Paquete de la API de inventario usada en la demostración de VERAUD."""

from .api import create_app
from .repository import Product, ProductRepository
from .service import InventoryService, PurchaseItem

__all__ = [
    "InventoryService",
    "Product",
    "ProductRepository",
    "PurchaseItem",
    "create_app",
]
