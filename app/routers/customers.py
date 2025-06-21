"""
Customer CRUD endpoints
"""
from typing import List, Optional
from fastapi import APIRouter, HTTPException, Query
from sqlmodel import select
from app.database import SessionDep
from app.models import Customer, CustomerCreate, CustomerUpdate, CustomerRead


router = APIRouter(prefix="/customers", tags=["customers"])


@router.get("/", response_model=List[CustomerRead])
def list_customers(
    session: SessionDep,
    skip: int = Query(0, ge=0, description="Number of records to skip"),
    limit: int = Query(100, ge=1, le=1000, description="Number of records to return")
) -> List[Customer]:
    """List all customers with pagination"""
    customers = session.exec(select(Customer).offset(skip).limit(limit)).all()
    return customers


@router.get("/{customer_id}", response_model=CustomerRead)
def get_customer(customer_id: int, session: SessionDep) -> Customer:
    """Get a customer by ID"""
    customer = session.get(Customer, customer_id)
    if not customer:
        raise HTTPException(status_code=404, detail="Customer not found")
    return customer


@router.post("/", response_model=CustomerRead, status_code=201)
def create_customer(customer: CustomerCreate, session: SessionDep) -> Customer:
    """Create a new customer"""
    # Check if email already exists
    existing_customer = session.exec(
        select(Customer).where(Customer.email == customer.email)
    ).first()
    
    if existing_customer:
        raise HTTPException(status_code=409, detail="Email already exists")
    
    db_customer = Customer.model_validate(customer)
    session.add(db_customer)
    session.commit()
    session.refresh(db_customer)
    return db_customer


@router.put("/{customer_id}", response_model=CustomerRead)
def update_customer(
    customer_id: int, 
    customer: CustomerUpdate, 
    session: SessionDep
) -> Customer:
    """Update a customer"""
    db_customer = session.get(Customer, customer_id)
    if not db_customer:
        raise HTTPException(status_code=404, detail="Customer not found")
    
    # Check if email is being updated and already exists
    if customer.email and customer.email != db_customer.email:
        existing_customer = session.exec(
            select(Customer).where(Customer.email == customer.email)
        ).first()
        if existing_customer:
            raise HTTPException(status_code=409, detail="Email already exists")
    
    customer_data = customer.model_dump(exclude_unset=True)
    for field, value in customer_data.items():
        setattr(db_customer, field, value)
    
    session.add(db_customer)
    session.commit()
    session.refresh(db_customer)
    return db_customer


@router.delete("/{customer_id}")
def delete_customer(customer_id: int, session: SessionDep) -> dict:
    """Delete a customer"""
    customer = session.get(Customer, customer_id)
    if not customer:
        raise HTTPException(status_code=404, detail="Customer not found")
    
    session.delete(customer)
    session.commit()
    return {"message": "Customer deleted successfully"}
