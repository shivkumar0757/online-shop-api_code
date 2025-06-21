"""
Category endpoint tests
"""
import pytest
from fastapi.testclient import TestClient


def test_create_category(client: TestClient):
    """Test creating a new category"""
    category_data = {
        "title": "Electronics",
        "description": "Electronic devices and gadgets"
    }
    
    response = client.post("/api/v1/categories/", json=category_data)
    assert response.status_code == 201
    
    data = response.json()
    assert data["title"] == category_data["title"]
    assert data["description"] == category_data["description"]
    assert "id" in data


def test_get_category(client: TestClient):
    """Test getting a category by ID"""
    # Create category first
    category_data = {
        "title": "Books",
        "description": "Books and literature"
    }
    create_response = client.post("/api/v1/categories/", json=category_data)
    category_id = create_response.json()["id"]
    
    # Get category
    response = client.get(f"/api/v1/categories/{category_id}")
    assert response.status_code == 200
    
    data = response.json()
    assert data["id"] == category_id
    assert data["title"] == category_data["title"]


def test_get_category_not_found(client: TestClient):
    """Test getting non-existent category"""
    response = client.get("/api/v1/categories/999")
    assert response.status_code == 404


def test_list_categories(client: TestClient):
    """Test listing categories"""
    # Create a few categories
    categories = [
        {"title": "Electronics", "description": "Electronic devices"},
        {"title": "Books", "description": "Books and literature"}
    ]
    
    for category_data in categories:
        client.post("/api/v1/categories/", json=category_data)
    
    # List categories
    response = client.get("/api/v1/categories/")
    assert response.status_code == 200
    
    data = response.json()
    assert len(data) >= len(categories)


def test_update_category(client: TestClient):
    """Test updating a category"""
    # Create category
    category_data = {
        "title": "Electronics",
        "description": "Electronic devices"
    }
    create_response = client.post("/api/v1/categories/", json=category_data)
    category_id = create_response.json()["id"]
    
    # Update category
    update_data = {
        "title": "Consumer Electronics",
        "description": "Consumer electronic devices and gadgets"
    }
    response = client.put(f"/api/v1/categories/{category_id}", json=update_data)
    assert response.status_code == 200
    
    data = response.json()
    assert data["title"] == update_data["title"]
    assert data["description"] == update_data["description"]


def test_update_category_not_found(client: TestClient):
    """Test updating non-existent category"""
    update_data = {
        "title": "Test Category",
        "description": "Test description"
    }
    response = client.put("/api/v1/categories/999", json=update_data)
    assert response.status_code == 404


def test_delete_category(client: TestClient):
    """Test deleting a category"""
    # Create category
    category_data = {
        "title": "Electronics",
        "description": "Electronic devices"
    }
    create_response = client.post("/api/v1/categories/", json=category_data)
    category_id = create_response.json()["id"]
    
    # Delete category
    response = client.delete(f"/api/v1/categories/{category_id}")
    assert response.status_code == 200
    
    # Verify category is deleted
    get_response = client.get(f"/api/v1/categories/{category_id}")
    assert get_response.status_code == 404


def test_delete_category_not_found(client: TestClient):
    """Test deleting non-existent category"""
    response = client.delete("/api/v1/categories/999")
    assert response.status_code == 404
