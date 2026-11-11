"""Capa HTTP de la API de inventario."""

from __future__ import annotations

from typing import Any

from fastapi import FastAPI, HTTPException, Response, status
from pydantic import BaseModel, ConfigDict, Field

from .service import InventoryService, PurchaseItem


class ProductCreate(BaseModel):
    """Datos de entrada para crear un producto."""

    name: str = Field(min_length=1)
    price: float = Field(ge=0)
    stock: int = Field(default=0, ge=0)
    ratings: list[float] = Field(default_factory=list)


class ProductResponse(BaseModel):
    """Representación pública de un producto."""

    model_config = ConfigDict(from_attributes=True)

    id: int
    name: str
    price: float
    stock: int
    ratings: list[float]


class StockUpdate(BaseModel):
    """Datos de entrada para actualizar el stock."""

    new_stock: int = Field(ge=0)


class PurchaseItemRequest(BaseModel):
    """Línea de compra recibida por la API."""

    product_id: int
    quantity: int = Field(gt=0)


class PurchaseRequest(BaseModel):
    """Solicitud de cálculo del total de una compra."""

    items: list[PurchaseItemRequest] = Field(default_factory=list)


class PasswordRequest(BaseModel):
    """Valor recibido para la validación de contraseña."""

    password: Any = Field(...)


def create_app(inventory_service: InventoryService | None = None) -> FastAPI:
    """Crea la aplicación FastAPI con un servicio de inventario inyectable."""
    service = inventory_service or InventoryService()
    app = FastAPI(title="VERAUD Inventory Demo", version="1.0.0")

    @app.get("/products", response_model=list[ProductResponse])
    def list_products() -> list[ProductResponse]:
        return service.list_products()

    @app.get("/products/{product_id}", response_model=ProductResponse)
    def get_product(product_id: int) -> ProductResponse:
        try:
            return service.get_product(product_id)
        except KeyError as exc:
            raise HTTPException(status_code=404, detail=str(exc)) from exc

    @app.post(
        "/products",
        response_model=ProductResponse,
        status_code=status.HTTP_201_CREATED,
    )
    def create_product(payload: ProductCreate) -> ProductResponse:
        try:
            return service.create_product(
                name=payload.name,
                price=payload.price,
                stock=payload.stock,
                ratings=payload.ratings,
            )
        except ValueError as exc:
            raise HTTPException(status_code=422, detail=str(exc)) from exc

    @app.patch("/products/{product_id}/stock", response_model=ProductResponse)
    def update_stock(product_id: int, payload: StockUpdate) -> ProductResponse:
        try:
            return service.update_stock(product_id, payload.new_stock)
        except ValueError as exc:
            raise HTTPException(status_code=422, detail=str(exc)) from exc
        except KeyError as exc:
            raise HTTPException(status_code=404, detail=str(exc)) from exc

    @app.delete(
        "/products/{product_id}",
        status_code=status.HTTP_204_NO_CONTENT,
    )
    def delete_product(product_id: int) -> Response:
        service.delete_product(product_id)
        return Response(status_code=status.HTTP_204_NO_CONTENT)

    @app.get("/products/{product_id}/average-rating")
    def average_rating(product_id: int) -> dict[str, float | None]:
        try:
            return {
                "product_id": product_id,
                "average_rating": service.average_rating(product_id),
            }
        except KeyError as exc:
            raise HTTPException(status_code=404, detail=str(exc)) from exc

    @app.post("/purchases/total")
    def purchase_total(payload: PurchaseRequest) -> dict[str, float]:
        items = [
            PurchaseItem(product_id=item.product_id, quantity=item.quantity)
            for item in payload.items
        ]
        try:
            return {"total": service.calculate_total(items)}
        except ValueError as exc:
            raise HTTPException(status_code=422, detail=str(exc)) from exc
        except KeyError as exc:
            raise HTTPException(status_code=404, detail=str(exc)) from exc

    @app.post("/passwords/validate")
    def validate_password(payload: PasswordRequest) -> dict[str, bool]:
        return {"valid": service.validate_password(payload.password)}

    return app


app = create_app()
