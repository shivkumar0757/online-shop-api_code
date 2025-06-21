"""
Shop item endpoint tests
"""
import pytest
from fastapi.testclient import TestClient


def test_create_shop_item(client: TestClient):
    """Test creating a new shop item"""
    # Create a category first
    category_data = {
        "title": "Electronics",
        "description": "Electronic devices"
    }
    category_response = client.post("/api/v1/categories/", json=category_data)
    category_id = category_response.json()["id"]
    
    # Create shop item
    item_data = {
        "title": "Smartphone",
        "description": "Latest model smartphone",
        "price": 699.99,
        "category_ids": [category_id]
    }
    
    response = client.post("/api/v1/items/", json=item_data)
    assert response.status_code == 201
    
    data = response.json()
    assert data["title"] == item_data["title"]
    assert data["description"] == item_data["description"]
    assert data["price"] == item_data["price"]
    assert "id" in data


def test_create_shop_item_without_categories(client: TestClient):
    """Test creating a shop item without categories"""
    item_data = {
        "title": "Generic Item",
        "description": "A generic item",
        "price": 19.99
    }
    
    response = client.post("/api/v1/items/", json=item_data)
    assert response.status_code == 201
    
    data = response.json()
    assert data["title"] == item_data["title"]
    assert data["price"] == item_data["price"]


def test_get_shop_item(client: TestClient):
    """Test getting a shop item by ID"""
    # Create item first
    item_data = {
        "title": "Test Item",
        "description": "Test description",
        "price": 29.99
    }
    create_response = client.post("/api/v1/items/", json=item_data)
    item_id = create_response.json()["id"]
    
    # Get item
    response = client.get(f"/api/v1/items/{item_id}")
    assert response.status_code == 200
    
    data = response.json()
    assert data["id"] == item_id
    assert data["title"] == item_data["title"]


def test_get_shop_item_not_found(client: TestClient):
    """Test getting non-existent shop item"""
    response = client.get("/api/v1/items/999")
    assert response.status_code == 404


def test_list_shop_items(client: TestClient):
    """Test listing shop items"""
    # Create a few items
    items = [
        {"title": "Item 1", "description": "Description 1", "price": 10.99},
        {"title": "Item 2", "description": "Description 2", "price": 20.99}
    ]
    
    for item_data in items:
        client.post("/api/v1/items/", json=item_data)
    
    # List items
    response = client.get("/api/v1/items/")
    assert response.status_code == 200
    
    data = response.json()
    assert len(data) >= len(items)


def test_list_shop_items_by_category(client: TestClient):
    """Test listing shop items filtered by category"""
    # Create categories
    category1_response = client.post("/api/v1/categories/", json={
        "title": "Category 1", "description": "First category"
    })
    category2_response = client.post("/api/v1/categories/", json={
        "title": "Category 2", "description": "Second category"
    })
    
    category1_id = category1_response.json()["id"]
    category2_id = category2_response.json()["id"]
    
    # Create items with different categories
    client.post("/api/v1/items/", json={
        "title": "Item 1", "description": "Description 1", "price": 10.99,
        "category_ids": [category1_id]
    })
    client.post("/api/v1/items/", json={
        "title": "Item 2", "description": "Description 2", "price": 20.99,
        "category_ids": [category2_id]
    })
    
    # Filter by category 1
    response = client.get(f"/api/v1/items/?category_id={category1_id}")
    assert response.status_code == 200
    
    data = response.json()
    assert len(data) >= 1


def test_update_shop_item(client: TestClient):
    """Test updating a shop item"""
    # Create item
    item_data = {
        "title": "Original Item",
        "description": "Original description",
        "price": 19.99
    }
    create_response = client.post("/api/v1/items/", json=item_data)
    item_id = create_response.json()["id"]
    
    # Update item
    update_data = {
        "title": "Updated Item",
        "description": "Updated description",
        "price": 29.99
    }
    response = client.put(f"/api/v1/items/{item_id}", json=update_data)
    assert response.status_code == 200
    
    data = response.json()
    assert data["title"] == update_data["title"]
    assert data["price"] == update_data["price"]


def test_update_shop_item_not_found(client: TestClient):
    """Test updating non-existent shop item"""
    update_data = {
        "title": "Test Item",
        "description": "Test description",
        "price": 19.99
    }
    response = client.put("/api/v1/items/999", json=update_data)
    assert response.status_code == 404


def test_delete_shop_item(client: TestClient):
    """Test deleting a shop item"""
    # Create item
    item_data = {
        "title": "Item to Delete",
        "description": "This item will be deleted",
        "price": 19.99
    }
    create_response = client.post("/api/v1/items/", json=item_data)
    item_id = create_response.json()["id"]
    
    # Delete item
    response = client.delete(f"/api/v1/items/{item_id}")
    assert response.status_code == 200
    
    # Verify item is deleted
    get_response = client.get(f"/api/v1/items/{item_id}")
    assert get_response.status_code == 404


def test_delete_shop_item_not_found(client: TestClient):
    """Test deleting non-existent shop item"""
    response = client.delete("/api/v1/items/999")
    assert response.status_code == 404
