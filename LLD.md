# Low Level Design (LLD)
## Online Shop Backend API

### 1. System Architecture

```
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│   API Layer    │    │  Business Layer │    │   Data Layer    │
│   (FastAPI)    │◄──►│   (Services)    │◄──►│   (SQLModel)    │
└─────────────────┘    └─────────────────┘    └─────────────────┘
```

### 2. Project Structure

```
backend-api/
├── app/
│   ├── __init__.py
│   ├── main.py                 # FastAPI application entry point
│   ├── models/
│   │   ├── __init__.py
│   │   ├── customer.py         # Customer data models
│   │   ├── shop_item.py        # ShopItem and Category models
│   │   └── order.py            # Order and OrderItem models
│   ├── routers/
│   │   ├── __init__.py
│   │   ├── customers.py        # Customer CRUD endpoints
│   │   ├── categories.py       # Category CRUD endpoints
│   │   ├── shop_items.py       # ShopItem CRUD endpoints
│   │   └── orders.py           # Order CRUD endpoints
│   ├── database/
│   │   ├── __init__.py
│   │   ├── connection.py       # Database connection setup
│   │   └── init_data.py        # Test data initialization
│   └── utils/
│       ├── __init__.py
│       └── responses.py        # Common response models
├── tests/
│   ├── __init__.py
│   ├── conftest.py            # Pytest configuration
│   ├── test_customers.py       # Customer endpoint tests
│   ├── test_categories.py      # Category endpoint tests
│   ├── test_shop_items.py      # ShopItem endpoint tests
│   └── test_orders.py          # Order endpoint tests
├── data/
│   └── test_data.json         # Sample test data
├── requirements.txt           # Python dependencies
├── task.md                   # Original task description
├── PRD.md                    # Product Requirements Document
├── LLD.md                    # This document
└── README.md                 # Setup and usage instructions
```

### 3. Database Design

#### 3.1 Entity Relationship Diagram

```
┌─────────────┐    ┌─────────────────┐    ┌─────────────────┐
│  Customer   │    │     Order       │    │   OrderItem     │
├─────────────┤    ├─────────────────┤    ├─────────────────┤
│ id (PK)     │◄───┤ id (PK)         │◄───┤ id (PK)         │
│ name        │    │ customer_id(FK) │    │ order_id (FK)   │
│ surname     │    │ created_at      │    │ shop_item_id(FK)│
│ email       │    └─────────────────┘    │ quantity        │
└─────────────┘                           └─────────────────┘
                                                    │
                    ┌─────────────────┐             │
                    │   ShopItem      │◄────────────┘
                    ├─────────────────┤
                    │ id (PK)         │
                    │ title           │
                    │ description     │
                    │ price           │
                    └─────────────────┘
                             │
                             │ Many-to-Many
                             ▼
                    ┌─────────────────┐
                    │ShopItemCategory │
                    ├─────────────────┤
                    │ id (PK)         │
                    │ title           │
                    │ description     │
                    └─────────────────┘
```

#### 3.2 Table Definitions

**customers**
```sql
CREATE TABLE customers (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name VARCHAR(100) NOT NULL,
    surname VARCHAR(100) NOT NULL,
    email VARCHAR(255) UNIQUE NOT NULL
);
```

**shop_item_categories**
```sql
CREATE TABLE shop_item_categories (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    title VARCHAR(200) NOT NULL,
    description TEXT NOT NULL
);
```

**shop_items**
```sql
CREATE TABLE shop_items (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    title VARCHAR(200) NOT NULL,
    description TEXT NOT NULL,
    price DECIMAL(10,2) NOT NULL CHECK (price > 0)
);
```

**shop_item_category_association**
```sql
CREATE TABLE shop_item_category_association (
    shop_item_id INTEGER,
    category_id INTEGER,
    FOREIGN KEY (shop_item_id) REFERENCES shop_items(id),
    FOREIGN KEY (category_id) REFERENCES shop_item_categories(id),
    PRIMARY KEY (shop_item_id, category_id)
);
```

**orders**
```sql
CREATE TABLE orders (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    customer_id INTEGER NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (customer_id) REFERENCES customers(id)
);
```

**order_items**
```sql
CREATE TABLE order_items (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    order_id INTEGER NOT NULL,
    shop_item_id INTEGER NOT NULL,
    quantity INTEGER NOT NULL CHECK (quantity > 0),
    FOREIGN KEY (order_id) REFERENCES orders(id),
    FOREIGN KEY (shop_item_id) REFERENCES shop_items(id)
);
```

### 4. API Design

#### 4.1 Common Response Models

```python
class SuccessResponse(BaseModel):
    success: bool = True
    data: Any

class ErrorResponse(BaseModel):
    success: bool = False
    error: str
    details: Optional[str] = None
```

#### 4.2 Data Models

**Customer Models**
```python
class CustomerBase(SQLModel):
    name: str = Field(max_length=100)
    surname: str = Field(max_length=100)
    email: str = Field(max_length=255, index=True)

class Customer(CustomerBase, table=True):
    __tablename__ = "customers"
    id: Optional[int] = Field(default=None, primary_key=True)

class CustomerCreate(CustomerBase):
    pass

class CustomerUpdate(CustomerBase):
    pass

class CustomerRead(CustomerBase):
    id: int
```

**Category Models**
```python
class CategoryBase(SQLModel):
    title: str = Field(max_length=200)
    description: str

class ShopItemCategory(CategoryBase, table=True):
    __tablename__ = "shop_item_categories"
    id: Optional[int] = Field(default=None, primary_key=True)

class CategoryCreate(CategoryBase):
    pass

class CategoryUpdate(CategoryBase):
    pass

class CategoryRead(CategoryBase):
    id: int
```

#### 4.3 Endpoint Specifications

**Customer Endpoints**
- `GET /api/v1/customers` - List customers (pagination support)
- `GET /api/v1/customers/{customer_id}` - Get customer by ID
- `POST /api/v1/customers` - Create customer
- `PUT /api/v1/customers/{customer_id}` - Update customer
- `DELETE /api/v1/customers/{customer_id}` - Delete customer

**Category Endpoints**
- `GET /api/v1/categories` - List categories
- `GET /api/v1/categories/{category_id}` - Get category by ID
- `POST /api/v1/categories` - Create category
- `PUT /api/v1/categories/{category_id}` - Update category
- `DELETE /api/v1/categories/{category_id}` - Delete category

**ShopItem Endpoints**
- `GET /api/v1/items` - List items (with category filter)
- `GET /api/v1/items/{item_id}` - Get item by ID
- `POST /api/v1/items` - Create item
- `PUT /api/v1/items/{item_id}` - Update item
- `DELETE /api/v1/items/{item_id}` - Delete item

**Order Endpoints**
- `GET /api/v1/orders` - List orders
- `GET /api/v1/orders/{order_id}` - Get order by ID
- `POST /api/v1/orders` - Create order
- `PUT /api/v1/orders/{order_id}` - Update order
- `DELETE /api/v1/orders/{order_id}` - Delete order

### 5. Implementation Strategy

#### 5.1 Development Phases

**Phase 1: Core Setup**
1. Set up FastAPI application structure
2. Configure SQLModel with SQLite
3. Create basic database models
4. Set up testing framework

**Phase 2: Customer Module**
1. Implement Customer models
2. Create Customer CRUD endpoints
3. Write Customer tests

**Phase 3: Category Module**
1. Implement Category models
2. Create Category CRUD endpoints
3. Write Category tests

**Phase 4: ShopItem Module**
1. Implement ShopItem models with category relationships
2. Create ShopItem CRUD endpoints
3. Write ShopItem tests

**Phase 5: Order Module**
1. Implement Order and OrderItem models
2. Create Order CRUD endpoints with complex relationships
3. Write Order tests

**Phase 6: Integration & Documentation**
1. Integration testing
2. Performance testing
3. Documentation updates
4. Sample data initialization

#### 5.2 Error Handling Strategy

```python
# Common HTTP exceptions
from fastapi import HTTPException

# 404 - Resource not found
raise HTTPException(status_code=404, detail="Customer not found")

# 422 - Validation error (handled automatically by FastAPI/Pydantic)

# 409 - Conflict (e.g., duplicate email)
raise HTTPException(status_code=409, detail="Email already exists")

# 500 - Internal server error
raise HTTPException(status_code=500, detail="Internal server error")
```

#### 5.3 Testing Strategy

**Unit Tests**
- Individual model validation
- Database operations
- Business logic functions

**Integration Tests**
- Full API endpoint testing
- Database transaction testing
- Error scenario testing

**Test Data Management**
- Separate test database
- Test data fixtures
- Database cleanup between tests

### 6. Configuration

#### 6.1 Environment Variables

```python
# Database configuration
DATABASE_URL = "sqlite:///./shop.db"
TEST_DATABASE_URL = "sqlite:///./test_shop.db"

# API configuration
API_V1_PREFIX = "/api/v1"
PROJECT_NAME = "Online Shop API"
VERSION = "1.0.0"
```

#### 6.2 Application Settings

```python
from pydantic import BaseSettings

class Settings(BaseSettings):
    database_url: str = "sqlite:///./shop.db"
    test_database_url: str = "sqlite:///./test_shop.db"
    api_v1_prefix: str = "/api/v1"
    project_name: str = "Online Shop API"
    version: str = "1.0.0"
    
    class Config:
        env_file = ".env"

settings = Settings()
```

### 7. Deployment Considerations

#### 7.1 Local Development
- SQLite file-based database
- Development server with auto-reload
- Debug mode enabled

#### 7.2 Production Ready Features
- Database connection pooling
- Proper logging configuration
- Health check endpoints
- Dockerization support

### 8. Security Considerations

- Input validation via Pydantic models
- SQL injection prevention via SQLModel/SQLAlchemy
- Email format validation
- Positive number validation for prices and quantities

### 9. Performance Optimizations

- Database indexing on frequently queried fields
- Pagination for list endpoints
- Efficient query patterns with SQLModel
- Connection pooling for database operations
