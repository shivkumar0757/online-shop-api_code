# Online Shop Backend API

A minimalistic backend web application for an online shop with full CRUD functionality and automated tests, built with Python FastAPI.

## Features

- **Full CRUD Operations** for all entities (Customer, ShopItemCategory, ShopItem, Order)
- **RESTful API** with clear endpoint structure
- **Automatic API Documentation** with Swagger UI
- **Data Validation** using Pydantic models
- **Database Persistence** with SQLite
- **Comprehensive Test Suite** with pytest
- **Test Data Initialization** for easy development

## API Entities

### Customer
- ID (integer, auto-generated)
- Name (string, required)
- Surname (string, required)
- Email (string, required, unique)

### ShopItemCategory
- ID (integer, auto-generated)
- Title (string, required)
- Description (string, required)

### ShopItem
- ID (integer, auto-generated)
- Title (string, required)
- Description (string, required)
- Price (float, required, positive)
- Categories (many-to-many relationship with ShopItemCategory)

### Order & OrderItem
- Order: Customer reference, creation timestamp
- OrderItem: Shop item reference, quantity

## API Endpoints

### Customers
- `GET /api/v1/customers/` - List all customers
- `GET /api/v1/customers/{id}` - Get customer by ID
- `POST /api/v1/customers/` - Create new customer
- `PUT /api/v1/customers/{id}` - Update customer
- `DELETE /api/v1/customers/{id}` - Delete customer

### Categories
- `GET /api/v1/categories/` - List all categories
- `GET /api/v1/categories/{id}` - Get category by ID
- `POST /api/v1/categories/` - Create new category
- `PUT /api/v1/categories/{id}` - Update category
- `DELETE /api/v1/categories/{id}` - Delete category

### Shop Items
- `GET /api/v1/items/` - List all items (with optional category filter)
- `GET /api/v1/items/{id}` - Get item by ID
- `POST /api/v1/items/` - Create new item
- `PUT /api/v1/items/{id}` - Update item
- `DELETE /api/v1/items/{id}` - Delete item

### Orders
- `GET /api/v1/orders/` - List all orders
- `GET /api/v1/orders/{id}` - Get order by ID
- `POST /api/v1/orders/` - Create new order
- `PUT /api/v1/orders/{id}` - Update order
- `DELETE /api/v1/orders/{id}` - Delete order

## Quick Start

### Prerequisites

- Python 3.8 or higher
- pip (Python package installer)

### Installation

1. **Clone/Navigate to the project directory:**
   ```bash
   cd backend-api
   ```

2. **Create and activate a virtual environment (recommended):**
   ```bash
   # Create virtual environment
   python -m venv venv
   
   # Activate virtual environment
   # On macOS/Linux:
   source venv/bin/activate
   # On Windows:
   # venv\\Scripts\\activate
   ```

3. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

### Running the Application

1. **Start the server:**
   ```bash
   # From the backend-api directory
   python -m app.main
   
   # Or using uvicorn directly:
   uvicorn app.main:app --reload
   ```

2. **Access the API:**
   - API Base URL: `http://localhost:8000`
   - Interactive API Documentation (Swagger UI): `http://localhost:8000/docs`
   - Alternative Documentation (ReDoc): `http://localhost:8000/redoc`

### Testing

Run the complete test suite:

```bash
# Run all tests
pytest

# Run tests with verbose output
pytest -v

# Run tests with coverage
pytest --cov=app

# Run specific test file
pytest tests/test_customers.py
```

### Sample API Usage

#### Create a Customer
```bash
curl -X POST "http://localhost:8000/api/v1/customers/" \
     -H "Content-Type: application/json" \
     -d '{
       "name": "John",
       "surname": "Doe", 
       "email": "john.doe@example.com"
     }'
```

#### Create a Category
```bash
curl -X POST "http://localhost:8000/api/v1/categories/" \
     -H "Content-Type: application/json" \
     -d '{
       "title": "Electronics",
       "description": "Electronic devices and gadgets"
     }'
```

#### Create a Shop Item
```bash
curl -X POST "http://localhost:8000/api/v1/items/" \
     -H "Content-Type: application/json" \
     -d '{
       "title": "Smartphone",
       "description": "Latest model smartphone",
       "price": 699.99,
       "category_ids": [1]
     }'
```

#### Create an Order
```bash
curl -X POST "http://localhost:8000/api/v1/orders/" \
     -H "Content-Type: application/json" \
     -d '{
       "customer_id": 1,
       "items": [
         {
           "shop_item_id": 1,
           "quantity": 2
         }
       ]
     }'
```

## Project Structure

```
backend-api/
├── app/
│   ├── __init__.py
│   ├── main.py              # FastAPI application entry point
│   ├── models/              # Data models (Pydantic/SQLModel)
│   │   ├── customer.py
│   │   ├── shop_item.py
│   │   └── order.py
│   ├── routers/             # API route handlers
│   │   ├── customers.py
│   │   ├── categories.py
│   │   ├── shop_items.py
│   │   └── orders.py
│   ├── database/            # Database configuration
│   │   ├── connection.py
│   │   └── init_data.py
│   └── utils/               # Utility functions
│       └── responses.py
├── tests/                   # Test suite
│   ├── conftest.py
│   ├── test_customers.py
│   ├── test_categories.py
│   ├── test_shop_items.py
│   └── test_orders.py
├── data/
│   └── test_data.json       # Sample test data
├── requirements.txt         # Python dependencies
├── PRD.md                   # Product Requirements Document
├── LLD.md                   # Low Level Design Document
├── task.md                  # Original task description
└── README.md               # This file
```

## Technology Stack

- **Framework:** FastAPI (Python web framework)
- **Database:** SQLite (file-based SQL database)
- **ORM:** SQLModel (combines SQLAlchemy + Pydantic)
- **Data Validation:** Pydantic
- **Testing:** pytest + FastAPI TestClient
- **Documentation:** Auto-generated OpenAPI/Swagger

## Development

### Adding New Features

1. **Models:** Add new data models in `app/models/`
2. **Routes:** Create API endpoints in `app/routers/`
3. **Tests:** Write tests in `tests/`
4. **Update Documentation:** Update this README as needed

### Database

- Database file: `shop.db` (created automatically)
- Test database: In-memory SQLite for tests
- Sample data is loaded automatically on first run

### Error Handling

The API returns appropriate HTTP status codes:
- `200` - Success
- `201` - Created
- `404` - Not Found
- `409` - Conflict (e.g., duplicate email)
- `422` - Validation Error

## Troubleshooting

### Common Issues

1. **Import Errors:** Make sure you're in the correct directory and virtual environment is activated
2. **Port Already in Use:** Change the port in `app/main.py` if 8000 is occupied
3. **Database Issues:** Delete `shop.db` file to reset the database

### Getting Help

1. Check the interactive API documentation at `/docs`
2. Review test files for usage examples
3. Check the logs in the terminal where the server is running

## License

This project is created for educational purposes as part of a programming assignment.