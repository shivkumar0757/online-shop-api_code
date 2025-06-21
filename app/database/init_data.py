"""
Test data initialization
"""
import json
from typing import List
from sqlmodel import Session
from app.models import (
    Customer, CustomerCreate,
    ShopItemCategory, CategoryCreate,
    ShopItem, ShopItemCreate,
    Order, OrderCreate, OrderItem
)


def load_test_data() -> dict:
    """Load test data from JSON file"""
    try:
        with open("data/test_data.json", "r") as f:
            return json.load(f)
    except FileNotFoundError:
        return get_default_test_data()


def get_default_test_data() -> dict:
    """Get default test data if file doesn't exist"""
    return {
        "customers": [
            {"name": "John", "surname": "Doe", "email": "john.doe@example.com"},
            {"name": "Jane", "surname": "Smith", "email": "jane.smith@example.com"},
            {"name": "Bob", "surname": "Johnson", "email": "bob.johnson@example.com"}
        ],
        "categories": [
            {"title": "Electronics", "description": "Electronic devices and gadgets"},
            {"title": "Books", "description": "Books and literature"},
            {"title": "Clothing", "description": "Apparel and accessories"},
            {"title": "Home & Garden", "description": "Home improvement and gardening items"}
        ],
        "shop_items": [
            {
                "title": "Smartphone",
                "description": "Latest model smartphone with advanced features",
                "price": 699.99,
                "category_ids": [1]
            },
            {
                "title": "Programming Book",
                "description": "Learn Python programming from basics to advanced",
                "price": 29.99,
                "category_ids": [2]
            },
            {
                "title": "T-Shirt",
                "description": "Comfortable cotton t-shirt",
                "price": 19.99,
                "category_ids": [3]
            },
            {
                "title": "Garden Tools Set",
                "description": "Complete set of essential garden tools",
                "price": 89.99,
                "category_ids": [4]
            },
            {
                "title": "Laptop",
                "description": "High-performance laptop for work and gaming",
                "price": 1299.99,
                "category_ids": [1]
            }
        ]
    }


def initialize_test_data(session: Session):
    """Initialize database with test data"""
    
    # Check if data already exists
    existing_customers = session.query(Customer).first()
    if existing_customers:
        print("Test data already exists, skipping initialization")
        return
    
    test_data = load_test_data()
    
    # Create customers
    customers = []
    for customer_data in test_data["customers"]:
        customer = Customer(**customer_data)
        session.add(customer)
        customers.append(customer)
    
    session.commit()
    
    # Create categories
    categories = []
    for category_data in test_data["categories"]:
        category = ShopItemCategory(**category_data)
        session.add(category)
        categories.append(category)
    
    session.commit()
    
    # Create shop items
    for item_data in test_data["shop_items"]:
        category_ids = item_data.pop("category_ids", [])
        item = ShopItem(**item_data)
        session.add(item)
        session.commit()
        session.refresh(item)
        
        # Add categories through association table
        from app.models.shop_item import ShopItemCategoryAssociation
        for category_id in category_ids:
            if category_id <= len(categories):
                association = ShopItemCategoryAssociation(
                    shop_item_id=item.id,
                    category_id=categories[category_id - 1].id
                )
                session.add(association)
        
        session.commit()
    
    print("Test data initialized successfully")
