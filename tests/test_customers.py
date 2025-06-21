"""
Customer endpoint tests
"""
import pytest
from fastapi.testclient import TestClient
from app.models import Customer


def test_create_customer(client: TestClient):
    """Test creating a new customer"""
    customer_data = {
        "name": "John",
        "surname": "Doe",
        "email": "john.doe@test.com"
    }
    
    response = client.post("/api/v1/customers/", json=customer_data)
    assert response.status_code == 201
    
    data = response.json()
    assert data["name"] == customer_data["name"]
    assert data["surname"] == customer_data["surname"]
    assert data["email"] == customer_data["email"]
    assert "id" in data


def test_create_customer_duplicate_email(client: TestClient):
    """Test creating customer with duplicate email"""
    customer_data = {
        "name": "John",
        "surname": "Doe",
        "email": "john.doe@test.com"
    }
    
    # Create first customer
    response = client.post("/api/v1/customers/", json=customer_data)
    assert response.status_code == 201
    
    # Try to create second customer with same email
    response = client.post("/api/v1/customers/", json=customer_data)
    assert response.status_code == 409


def test_get_customer(client: TestClient):
    """Test getting a customer by ID"""
    # Create customer first
    customer_data = {
        "name": "Jane",
        "surname": "Smith",
        "email": "jane.smith@test.com"
    }
    create_response = client.post("/api/v1/customers/", json=customer_data)
    customer_id = create_response.json()["id"]
    
    # Get customer
    response = client.get(f"/api/v1/customers/{customer_id}")
    assert response.status_code == 200
    
    data = response.json()
    assert data["id"] == customer_id
    assert data["name"] == customer_data["name"]


def test_get_customer_not_found(client: TestClient):
    """Test getting non-existent customer"""
    response = client.get("/api/v1/customers/999")
    assert response.status_code == 404


def test_list_customers(client: TestClient):
    """Test listing customers"""
    # Create a few customers
    customers = [
        {"name": "John", "surname": "Doe", "email": "john@test.com"},
        {"name": "Jane", "surname": "Smith", "email": "jane@test.com"}
    ]
    
    for customer_data in customers:
        client.post("/api/v1/customers/", json=customer_data)
    
    # List customers
    response = client.get("/api/v1/customers/")
    assert response.status_code == 200
    
    data = response.json()
    assert len(data) >= len(customers)


def test_update_customer(client: TestClient):
    """Test updating a customer"""
    # Create customer
    customer_data = {
        "name": "John",
        "surname": "Doe",
        "email": "john@test.com"
    }
    create_response = client.post("/api/v1/customers/", json=customer_data)
    customer_id = create_response.json()["id"]
    
    # Update customer
    update_data = {
        "name": "Johnny",
        "surname": "Doe",
        "email": "johnny@test.com"
    }
    response = client.put(f"/api/v1/customers/{customer_id}", json=update_data)
    assert response.status_code == 200
    
    data = response.json()
    assert data["name"] == update_data["name"]
    assert data["email"] == update_data["email"]


def test_update_customer_not_found(client: TestClient):
    """Test updating non-existent customer"""
    update_data = {
        "name": "John",
        "surname": "Doe",
        "email": "john@test.com"
    }
    response = client.put("/api/v1/customers/999", json=update_data)
    assert response.status_code == 404


def test_delete_customer(client: TestClient):
    """Test deleting a customer"""
    # Create customer
    customer_data = {
        "name": "John",
        "surname": "Doe",
        "email": "john@test.com"
    }
    create_response = client.post("/api/v1/customers/", json=customer_data)
    customer_id = create_response.json()["id"]
    
    # Delete customer
    response = client.delete(f"/api/v1/customers/{customer_id}")
    assert response.status_code == 200
    
    # Verify customer is deleted
    get_response = client.get(f"/api/v1/customers/{customer_id}")
    assert get_response.status_code == 404


def test_delete_customer_not_found(client: TestClient):
    """Test deleting non-existent customer"""
    response = client.delete("/api/v1/customers/999")
    assert response.status_code == 404
