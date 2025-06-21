"""
Customer data models
"""
from typing import Optional
from sqlmodel import SQLModel, Field


class CustomerBase(SQLModel):
    """Base customer model with common fields"""
    name: str = Field(max_length=100, description="Customer's first name")
    surname: str = Field(max_length=100, description="Customer's last name") 
    email: str = Field(max_length=255, index=True, description="Customer's email address")


class Customer(CustomerBase, table=True):
    """Customer database model"""
    __tablename__ = "customers"
    
    id: Optional[int] = Field(default=None, primary_key=True, description="Customer ID")


class CustomerCreate(CustomerBase):
    """Customer creation model"""
    pass


class CustomerUpdate(CustomerBase):
    """Customer update model - all fields optional"""
    name: Optional[str] = Field(default=None, max_length=100)
    surname: Optional[str] = Field(default=None, max_length=100)
    email: Optional[str] = Field(default=None, max_length=255)


class CustomerRead(CustomerBase):
    """Customer read model with ID"""
    id: int
