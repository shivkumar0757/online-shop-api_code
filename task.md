# Task 1: Backend API

## Overview
Create a minimalistic backend web application for an online shop with full CRUD functionality and automated tests.

## Requirements

### Data Entities

#### Customer
- ID (integer)
- Name (string)
- Surname (string)
- Email (string)

#### ShopItemCategory
- ID (integer)
- Title (string)
- Description (string)

#### ShopItem
- ID (integer)
- Title (string)
- Description (string)
- Price (float)
- Category (list of ShopItemCategory)

#### OrderItem
- ID (integer)
- ShopItem (ShopItem)
- Quantity (integer)

#### Order
- ID (integer)
- Customer (Customer)
- Items (list of OrderItem)

### Implementation Requirements

1. **CRUD APIs**: Implement full Create, Read, Update, Delete operations for:
   - Customer
   - ShopItemCategory
   - ShopItem
   - Order

2. **Endpoint Testing**: Create automated tests for each endpoint

3. **Data Persistence**: 
   - Use any data persistence implementation (database, in-memory, file-based)
   - Include initialization of test data

4. **Documentation**: Include instructions for:
   - Project setup
   - Running the application
   - Running tests

## Deliverables

- Complete backend API implementation
- Automated test suite
- Test data initialization
- Clear documentation

## Technology Choices

You are free to use any:
- Programming language
- Web framework
- Database or persistence solution
- Testing framework

## Getting Started

Create your implementation in this directory following the requirements above.