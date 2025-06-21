"""
Order and order item data models
"""
from typing import Optional, List
from datetime import datetime
from sqlmodel import SQLModel, Field


class OrderItemBase(SQLModel):
    """Base order item model"""
    shop_item_id: int = Field(foreign_key="shop_items.id", description="Shop item ID")
    quantity: int = Field(gt=0, description="Item quantity (must be positive)")


class OrderItem(OrderItemBase, table=True):
    """Order item database model"""
    __tablename__ = "order_items"
    
    id: Optional[int] = Field(default=None, primary_key=True, description="Order item ID")
    order_id: int = Field(foreign_key="orders.id", description="Order ID")


class OrderItemCreate(OrderItemBase):
    """Order item creation model"""
    pass


class OrderItemRead(OrderItemBase):
    """Order item read model"""
    id: int
    order_id: int


class OrderBase(SQLModel):
    """Base order model"""
    customer_id: int = Field(foreign_key="customers.id", description="Customer ID")


class Order(OrderBase, table=True):
    """Order database model"""
    __tablename__ = "orders"
    
    id: Optional[int] = Field(default=None, primary_key=True, description="Order ID")
    created_at: Optional[datetime] = Field(default_factory=datetime.utcnow, description="Order creation timestamp")


class OrderCreate(OrderBase):
    """Order creation model"""
    items: List[OrderItemCreate] = Field(description="List of order items")


class OrderUpdate(SQLModel):
    """Order update model"""
    customer_id: Optional[int] = Field(default=None, foreign_key="customers.id")
    items: Optional[List[OrderItemCreate]] = Field(default=None, description="List of order items")


class OrderRead(OrderBase):
    """Order read model with relationships"""
    id: int
    created_at: datetime
    items: List[OrderItemRead] = []
