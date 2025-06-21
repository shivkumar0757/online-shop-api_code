"""
Order endpoint tests
"""
import pytest
from fastapi.testclient import TestClient


def test_create_order(client: TestClient):
    """Test creating a new order"""
    # Create customer
    customer_data = {
        "name": "John",
        "surname": "Doe",
        "email": "john@test.com"
    }
    customer_response = client.post("/api/v1/customers/", json=customer_data)
    customer_id = customer_response.json()["id"]
    
    # Create shop item
    item_data = {
        "title": "Test Item",
        "description": "Test description",
        "price": 19.99
    }
    item_response = client.post("/api/v1/items/", json=item_data)
    item_id = item_response.json()["id"]
    
    # Create order
    order_data = {
        "customer_id": customer_id,
        "items": [
            {
                "shop_item_id": item_id,
                "quantity": 2
            }
        ]
    }
    
    response = client.post("/api/v1/orders/", json=order_data)
    assert response.status_code == 201
    
    data = response.json()
    assert data["customer_id"] == customer_id
    assert "id" in data
    assert "created_at" in data


def test_create_order_invalid_customer(client: TestClient):
    """Test creating order with invalid customer"""
    # Create shop item
    item_data = {
        "title": "Test Item",
        "description": "Test description",
        "price": 19.99
    }
    item_response = client.post("/api/v1/items/", json=item_data)
    item_id = item_response.json()["id"]
    
    # Try to create order with non-existent customer
    order_data = {
        "customer_id": 999,
        "items": [
            {
                "shop_item_id": item_id,
                "quantity": 1
            }
        ]
    }
    
    response = client.post("/api/v1/orders/", json=order_data)
    assert response.status_code == 404


def test_create_order_invalid_item(client: TestClient):
    """Test creating order with invalid shop item"""
    # Create customer
    customer_data = {
        "name": "Jane",
        "surname": "Smith",
        "email": "jane@test.com"
    }
    customer_response = client.post("/api/v1/customers/", json=customer_data)
    customer_id = customer_response.json()["id"]
    
    # Try to create order with non-existent item
    order_data = {
        "customer_id": customer_id,
        "items": [
            {
                "shop_item_id": 999,
                "quantity": 1
            }
        ]
    }
    
    response = client.post("/api/v1/orders/", json=order_data)
    assert response.status_code == 404


def test_get_order(client: TestClient):
    """Test getting an order by ID"""
    # Create customer and item first
    customer_response = client.post("/api/v1/customers/", json={
        "name": "Test", "surname": "User", "email": "test@test.com"
    })
    item_response = client.post("/api/v1/items/", json={
        "title": "Test Item", "description": "Test", "price": 10.99
    })
    
    customer_id = customer_response.json()["id"]
    item_id = item_response.json()["id"]
    
    # Create order
    order_data = {
        "customer_id": customer_id,
        "items": [{"shop_item_id": item_id, "quantity": 1}]
    }
    create_response = client.post("/api/v1/orders/", json=order_data)
    order_id = create_response.json()["id"]
    
    # Get order
    response = client.get(f"/api/v1/orders/{order_id}")
    assert response.status_code == 200
    
    data = response.json()
    assert data["id"] == order_id
    assert data["customer_id"] == customer_id


def test_get_order_not_found(client: TestClient):
    """Test getting non-existent order"""
    response = client.get("/api/v1/orders/999")
    assert response.status_code == 404


def test_list_orders(client: TestClient):
    """Test listing orders"""
    # Create customer and item
    customer_response = client.post("/api/v1/customers/", json={
        "name": "Test", "surname": "User", "email": "test2@test.com"
    })
    item_response = client.post("/api/v1/items/", json={
        "title": "Test Item", "description": "Test", "price": 10.99
    })
    
    customer_id = customer_response.json()["id"]
    item_id = item_response.json()["id"]
    
    # Create a few orders
    orders = [
        {
            "customer_id": customer_id,
            "items": [{"shop_item_id": item_id, "quantity": 1}]
        },
        {
            "customer_id": customer_id,
            "items": [{"shop_item_id": item_id, "quantity": 2}]
        }
    ]
    
    for order_data in orders:
        client.post("/api/v1/orders/", json=order_data)
    
    # List orders
    response = client.get("/api/v1/orders/")
    assert response.status_code == 200
    
    data = response.json()
    assert len(data) >= len(orders)


def test_update_order(client: TestClient):
    """Test updating an order"""
    # Create customer and items
    customer1_response = client.post("/api/v1/customers/", json={
        "name": "Customer", "surname": "One", "email": "customer1@test.com"
    })
    customer2_response = client.post("/api/v1/customers/", json={
        "name": "Customer", "surname": "Two", "email": "customer2@test.com"
    })
    item_response = client.post("/api/v1/items/", json={
        "title": "Test Item", "description": "Test", "price": 10.99
    })
    
    customer1_id = customer1_response.json()["id"]
    customer2_id = customer2_response.json()["id"]
    item_id = item_response.json()["id"]
    
    # Create order
    order_data = {
        "customer_id": customer1_id,
        "items": [{"shop_item_id": item_id, "quantity": 1}]
    }
    create_response = client.post("/api/v1/orders/", json=order_data)
    order_id = create_response.json()["id"]
    
    # Update order
    update_data = {
        "customer_id": customer2_id,
        "items": [{"shop_item_id": item_id, "quantity": 3}]
    }
    response = client.put(f"/api/v1/orders/{order_id}", json=update_data)
    assert response.status_code == 200
    
    data = response.json()
    assert data["customer_id"] == customer2_id


def test_update_order_not_found(client: TestClient):
    """Test updating non-existent order"""
    update_data = {
        "customer_id": 1,
        "items": []
    }
    response = client.put("/api/v1/orders/999", json=update_data)
    assert response.status_code == 404


def test_delete_order(client: TestClient):
    """Test deleting an order"""
    # Create customer and item
    customer_response = client.post("/api/v1/customers/", json={
        "name": "Test", "surname": "User", "email": "delete@test.com"
    })
    item_response = client.post("/api/v1/items/", json={
        "title": "Test Item", "description": "Test", "price": 10.99
    })
    
    customer_id = customer_response.json()["id"]
    item_id = item_response.json()["id"]
    
    # Create order
    order_data = {
        "customer_id": customer_id,
        "items": [{"shop_item_id": item_id, "quantity": 1}]
    }
    create_response = client.post("/api/v1/orders/", json=order_data)
    order_id = create_response.json()["id"]
    
    # Delete order
    response = client.delete(f"/api/v1/orders/{order_id}")
    assert response.status_code == 200
    
    # Verify order is deleted
    get_response = client.get(f"/api/v1/orders/{order_id}")
    assert get_response.status_code == 404


def test_delete_order_not_found(client: TestClient):
    """Test deleting non-existent order"""
    response = client.delete("/api/v1/orders/999")
    assert response.status_code == 404
