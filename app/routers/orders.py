"""
Order CRUD endpoints
"""
from typing import List
from fastapi import APIRouter, HTTPException, Query
from sqlmodel import select
from app.database import SessionDep
from app.models import (
    Order, OrderCreate, OrderUpdate, OrderRead,
    OrderItem, Customer, ShopItem
)


router = APIRouter(prefix="/orders", tags=["orders"])


@router.get("/", response_model=List[OrderRead])
def list_orders(
    session: SessionDep,
    skip: int = Query(0, ge=0, description="Number of records to skip"),
    limit: int = Query(100, ge=1, le=1000, description="Number of records to return")
) -> List[Order]:
    """List all orders with pagination"""
    orders = session.exec(select(Order).offset(skip).limit(limit)).all()
    return orders


@router.get("/{order_id}", response_model=OrderRead)
def get_order(order_id: int, session: SessionDep) -> Order:
    """Get an order by ID"""
    order = session.get(Order, order_id)
    if not order:
        raise HTTPException(status_code=404, detail="Order not found")
    return order


@router.post("/", response_model=OrderRead, status_code=201)
def create_order(order: OrderCreate, session: SessionDep) -> Order:
    """Create a new order"""
    # Verify customer exists
    customer = session.get(Customer, order.customer_id)
    if not customer:
        raise HTTPException(status_code=404, detail="Customer not found")
    
    # Create the order
    order_data = order.model_dump(exclude={"items"})
    db_order = Order(**order_data)
    session.add(db_order)
    session.commit()
    session.refresh(db_order)
    
    # Create order items
    for item_data in order.items:
        # Verify shop item exists
        shop_item = session.get(ShopItem, item_data.shop_item_id)
        if not shop_item:
            raise HTTPException(
                status_code=404, 
                detail=f"Shop item with ID {item_data.shop_item_id} not found"
            )
        
        order_item = OrderItem(
            order_id=db_order.id,
            shop_item_id=item_data.shop_item_id,
            quantity=item_data.quantity
        )
        session.add(order_item)
    
    session.commit()
    session.refresh(db_order)
    return db_order


@router.put("/{order_id}", response_model=OrderRead)
def update_order(
    order_id: int,
    order: OrderUpdate,
    session: SessionDep
) -> Order:
    """Update an order"""
    db_order = session.get(Order, order_id)
    if not db_order:
        raise HTTPException(status_code=404, detail="Order not found")
    
    # Update customer if provided
    if order.customer_id:
        customer = session.get(Customer, order.customer_id)
        if not customer:
            raise HTTPException(status_code=404, detail="Customer not found")
        db_order.customer_id = order.customer_id
    
    # Update items if provided
    if order.items is not None:
        # Delete existing order items
        existing_items = session.exec(
            select(OrderItem).where(OrderItem.order_id == order_id)
        ).all()
        for item in existing_items:
            session.delete(item)
        
        # Create new order items
        for item_data in order.items:
            shop_item = session.get(ShopItem, item_data.shop_item_id)
            if not shop_item:
                raise HTTPException(
                    status_code=404,
                    detail=f"Shop item with ID {item_data.shop_item_id} not found"
                )
            
            order_item = OrderItem(
                order_id=db_order.id,
                shop_item_id=item_data.shop_item_id,
                quantity=item_data.quantity
            )
            session.add(order_item)
    
    session.add(db_order)
    session.commit()
    session.refresh(db_order)
    return db_order


@router.delete("/{order_id}")
def delete_order(order_id: int, session: SessionDep) -> dict:
    """Delete an order"""
    order = session.get(Order, order_id)
    if not order:
        raise HTTPException(status_code=404, detail="Order not found")
    
    session.delete(order)
    session.commit()
    return {"message": "Order deleted successfully"}
