"""Pruebas funcionales de la API de inventario.

Las pruebas marcadas con ``_expected_failure`` describen el comportamiento
correcto exigido por los requisitos. Fracasan de forma intencional porque el
código contiene los defectos solicitados para la demostración de VERAUD.
"""

from __future__ import annotations

import pytest
from fastapi.testclient import TestClient

from inventory.api import create_app
from inventory.repository import ProductRepository
from inventory.service import InventoryService, PurchaseItem


@pytest.fixture
def repository() -> ProductRepository:
    repo = ProductRepository()
    repo.add_product("Teclado", 50.0, 10, [4.0, 5.0])
    repo.add_product("Mouse", 20.0, 5, [3.0, 5.0])
    return repo


@pytest.fixture
def service(repository: ProductRepository) -> InventoryService:
    return InventoryService(repository)


@pytest.fixture
def client(service: InventoryService) -> TestClient:
    return TestClient(create_app(service))


# REQ-01: listar productos
def test_req01_list_products(service: InventoryService) -> None:
    products = service.list_products()

    assert [product.name for product in products] == ["Teclado", "Mouse"]
    assert len(products) == 2


def test_req01_list_products_empty() -> None:
    service = InventoryService(ProductRepository())

    assert service.list_products() == []


def test_req01_list_products_api(client: TestClient) -> None:
    response = client.get("/products")

    assert response.status_code == 200
    assert [item["name"] for item in response.json()] == ["Teclado", "Mouse"]


# REQ-02: consultar productos por ID
def test_req02_get_product_by_id_expected_failure(service: InventoryService) -> None:
    product = service.get_product(1)

    assert product.id == 1
    assert product.name == "Teclado"
    assert product.price == 50.0


# REQ-03: crear productos con validación
def test_req03_create_product_valid(service: InventoryService) -> None:
    product = service.create_product("Monitor", 150.0, 3, [4.5, 5.0])

    assert product.id == 3
    assert product.name == "Monitor"
    assert product.stock == 3
    assert service.repository.get_product_by_id(3) is product


def test_req03_create_product_api_valid(client: TestClient) -> None:
    response = client.post(
        "/products",
        json={"name": "Monitor", "price": 150.0, "stock": 3, "ratings": [5.0]},
    )

    assert response.status_code == 201
    assert response.json()["id"] == 3
    assert response.json()["name"] == "Monitor"


def test_req03_create_product_rejects_empty_name(service: InventoryService) -> None:
    with pytest.raises(ValueError):
        service.create_product("   ", 10.0, 1)


def test_req03_create_product_rejects_negative_price(service: InventoryService) -> None:
    with pytest.raises(ValueError):
        service.create_product("Monitor", -1.0, 1)


def test_req03_create_product_rejects_negative_stock(service: InventoryService) -> None:
    with pytest.raises(ValueError):
        service.create_product("Monitor", 10.0, -1)


def test_req03_create_product_rejects_invalid_rating(
    service: InventoryService,
) -> None:
    with pytest.raises(ValueError):
        service.create_product("Monitor", 10.0, 1, [5.5])


def test_req03_create_product_api_rejects_invalid_payload(
    client: TestClient,
) -> None:
    response = client.post(
        "/products",
        json={"name": "", "price": -1.0, "stock": -1},
    )

    assert response.status_code == 422


# REQ-04: actualizar stock sin permitir valores negativos
def test_req04_update_stock(service: InventoryService) -> None:
    product = service.update_stock(1, 4)

    assert product.stock == 4
    assert service.repository.get_product_by_id(1).stock == 4


def test_req04_update_stock_boundary_zero(service: InventoryService) -> None:
    product = service.update_stock(1, 0)

    assert product.stock == 0


def test_req04_update_stock_rejects_negative(service: InventoryService) -> None:
    with pytest.raises(ValueError):
        service.update_stock(1, -1)

    assert service.repository.get_product_by_id(1).stock == 10


def test_req04_update_stock_rejects_unknown_product(service: InventoryService) -> None:
    with pytest.raises(KeyError):
        service.update_stock(999, 1)


def test_req04_update_stock_api_negative(client: TestClient) -> None:
    response = client.patch("/products/1/stock", json={"new_stock": -1})

    assert response.status_code == 422


def test_req04_update_stock_api_valid(client: TestClient) -> None:
    response = client.patch("/products/1/stock", json={"new_stock": 7})

    assert response.status_code == 200
    assert response.json()["stock"] == 7


# REQ-05: eliminar productos
def test_req05_delete_product_expected_failure(service: InventoryService) -> None:
    service.delete_product(1)

    assert service.repository.get_product_by_id(1) is None
    assert len(service.list_products()) == 1


# REQ-06: calcular promedio de valoraciones
def test_req06_average_rating_expected_failure(service: InventoryService) -> None:
    average = service.average_rating(1)

    assert average == pytest.approx(4.5)


# REQ-07: calcular correctamente el total de una compra
def test_req07_calculate_total_single_unit(service: InventoryService) -> None:
    total = service.calculate_total([PurchaseItem(product_id=1, quantity=1)])

    assert total == pytest.approx(50.0)


def test_req07_calculate_total_empty_purchase(service: InventoryService) -> None:
    total = service.calculate_total([])

    assert total == pytest.approx(0.0)


def test_req07_calculate_total_rejects_zero_quantity(
    service: InventoryService,
) -> None:
    with pytest.raises(ValueError):
        service.calculate_total([PurchaseItem(product_id=1, quantity=0)])


def test_req07_calculate_total_multiple_quantities_expected_failure(
    service: InventoryService,
) -> None:
    total = service.calculate_total(
        [
            PurchaseItem(product_id=1, quantity=2),
            PurchaseItem(product_id=2, quantity=3),
        ]
    )

    assert total == pytest.approx(160.0)


def test_req07_calculate_total_api_expected_failure(client: TestClient) -> None:
    response = client.post(
        "/purchases/total",
        json={
            "items": [
                {"product_id": 1, "quantity": 2},
                {"product_id": 2, "quantity": 3},
            ]
        },
    )

    assert response.status_code == 200
    assert response.json()["total"] == pytest.approx(160.0)


# REQ-08: validar contraseñas de mínimo ocho caracteres
def test_req08_validate_password_boundaries(service: InventoryService) -> None:
    assert service.validate_password("12345678") is True
    assert service.validate_password("1234567") is False


def test_req08_validate_password_empty(service: InventoryService) -> None:
    assert service.validate_password("") is False


def test_req08_validate_password_rejects_non_string(
    service: InventoryService,
) -> None:
    assert service.validate_password(None) is False  # type: ignore[arg-type]


def test_req08_validate_password_api_rejects_non_string_values(
    client: TestClient,
) -> None:
    non_string_values = [None, 12345678, True, [], {}]

    for value in non_string_values:
        response = client.post("/passwords/validate", json={"password": value})

        assert response.status_code == 200
        assert response.json() == {"valid": False}


def test_req08_validate_password_api(client: TestClient) -> None:
    valid_response = client.post("/passwords/validate", json={"password": "abcdefgh"})
    invalid_response = client.post(
        "/passwords/validate",
        json={"password": "abcdefg"},
    )

    assert valid_response.status_code == 200
    assert valid_response.json() == {"valid": True}
    assert invalid_response.status_code == 200
    assert invalid_response.json() == {"valid": False}
