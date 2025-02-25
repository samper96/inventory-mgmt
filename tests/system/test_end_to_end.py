"""End to end system tests for the Inventory Management System FastAPI server."""

import requests

BASE_URL = "http://localhost:8000"


def test_insert_product():
    """
    Test inserting a new product via the /products endpoint.
    """
    # GIVEN
    payload = {"name": "Test Product", "stock": 100}

    # WHEN
    response = requests.post(f"{BASE_URL}/products/", json=payload)
    assert response.status_code == 200

    # THEN
    data = response.json()
    assert data["name"] == "Test Product"
    assert data["stock"] == 100
    assert "id" in data


def test_get_product():
    """
    Test retrieving a product by ID.
    """
    # GIVEN
    insert_resp = requests.post(f"{BASE_URL}/products/", json={"name": "Test Product", "stock": 50})
    assert insert_resp.status_code == 200
    inserted_product = insert_resp.json()
    assert "id" in inserted_product
    product_id = inserted_product["id"]

    # WHEN
    get_resp = requests.get(f"{BASE_URL}/products/{product_id}")
    assert get_resp.status_code == 200

    # THEN
    product = get_resp.json()
    assert product["name"] == "Test Product"
    assert product["stock"] == 50
    assert product["id"] == product_id


def test_update_product_stock():
    """
    End-to-end test for updating a product's stock.
    """
    # GIVEN
    create_resp = requests.post(f"{BASE_URL}/products/", json={"name": "StockUpdateItem", "stock": 5})
    assert create_resp.status_code == 200, "Failed to create product for stock update"
    product_data = create_resp.json()
    product_id = product_data["id"]

    # WHEN
    new_stock = 15
    update_resp = requests.put(f"{BASE_URL}/products/{product_id}?stock={new_stock}")
    assert update_resp.status_code == 200, "Failed to update product stock"

    # THEN
    updated_data = update_resp.json()
    assert updated_data["id"] == product_id
    assert updated_data["stock"] == new_stock, f"Expected stock to be {new_stock}, got {updated_data['stock']}"
