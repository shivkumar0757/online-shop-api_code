# Product Requirements Document (PRD)
## Online Shop Backend API

### 1. Project Overview
Create a minimalistic backend web application for an online shop with full CRUD functionality and automated tests using Python FastAPI.

### 2. Functional Requirements

#### 2.1 Data Entities

**Customer**
- ID (integer, auto-generated primary key)
- Name (string, required)
- Surname (string, required)  
- Email (string, required, unique)

**ShopItemCategory**
- ID (integer, auto-generated primary key)
- Title (string, required)
- Description (string, required)

**ShopItem**
- ID (integer, auto-generated primary key)
- Title (string, required)
- Description (string, required)
- Price (float, required, positive value)
- Category (list of ShopItemCategory, many-to-many relationship)

**OrderItem**
- ID (integer, auto-generated primary key)
- ShopItem (reference to ShopItem)
- Quantity (integer, required, positive value)

**Order**
- ID (integer, auto-generated primary key)
- Customer (reference to Customer)
- Items (list of OrderItem, one-to-many relationship)

#### 2.2 API Endpoints

**Customer CRUD**
- GET /customers - List all customers
- GET /customers/{id} - Get customer by ID
- POST /customers - Create new customer
- PUT /customers/{id} - Update customer
- DELETE /customers/{id} - Delete customer

**ShopItemCategory CRUD**
- GET /categories - List all categories
- GET /categories/{id} - Get category by ID
- POST /categories - Create new category
- PUT /categories/{id} - Update category
- DELETE /categories/{id} - Delete category

**ShopItem CRUD**
- GET /items - List all items (with optional category filter)
- GET /items/{id} - Get item by ID
- POST /items - Create new item
- PUT /items/{id} - Update item
- DELETE /items/{id} - Delete item

**Order CRUD**
- GET /orders - List all orders
- GET /orders/{id} - Get order by ID
- POST /orders - Create new order
- PUT /orders/{id} - Update order
- DELETE /orders/{id} - Delete order

### 3. Technical Requirements

#### 3.1 Framework & Technology Stack
- **Backend Framework**: FastAPI (Python)
- **Database**: SQLite (for simplicity)
- **ORM**: SQLModel (combines SQLAlchemy + Pydantic)
- **Testing**: pytest with FastAPI TestClient
- **Data Validation**: Pydantic models
- **Documentation**: Auto-generated OpenAPI/Swagger docs

#### 3.2 Data Persistence
- SQLite database file for data storage
- Database initialization with test data
- Foreign key constraints for relationships
- Database migrations (if needed)

#### 3.3 Error Handling
- HTTP status codes (200, 201, 404, 422, 500)
- Validation error responses
- Proper error messages

#### 3.4 Testing Requirements
- Unit tests for all CRUD operations
- Integration tests for endpoints
- Test data setup and teardown
- Test coverage for error scenarios

### 4. Quality Requirements

#### 4.1 Performance
- Response time under 100ms for simple CRUD operations
- Support for pagination on list endpoints

#### 4.2 Reliability
- Proper error handling and validation
- Database transaction integrity

#### 4.3 Maintainability
- Clean code structure with separation of concerns
- Comprehensive documentation
- Type hints throughout codebase

### 5. Deliverables

1. **Source Code**
   - Complete FastAPI application
   - Modular project structure
   - Configuration files

2. **Tests**
   - Comprehensive test suite
   - Test documentation

3. **Documentation**
   - Setup and installation guide
   - API usage examples
   - Development guidelines

4. **Data**
   - Sample test data
   - Database initialization scripts

### 6. Success Criteria

- All CRUD operations working correctly
- All tests passing
- API documentation accessible via Swagger UI
- Easy setup and deployment process
- Clean, maintainable code structure

### 7. Out of Scope

- User authentication/authorization
- Real-time features
- File upload functionality
- Email notifications
- Advanced search features
- Payment processing
- Multi-tenancy
