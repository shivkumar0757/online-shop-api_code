"""
Shop item CRUD endpoints
"""
from typing import List, Optional
from fastapi import APIRouter, HTTPException, Query
from sqlmodel import select
from app.database import SessionDep
from app.models import (
    ShopItem, ShopItemCreate, ShopItemUpdate, ShopItemRead,
    ShopItemCategory, ShopItemCategoryAssociation
)


router = APIRouter(prefix="/items", tags=["items"])


@router.get("/", response_model=List[ShopItemRead])
def list_shop_items(
    session: SessionDep,
    category_id: Optional[int] = Query(None, description="Filter by category ID"),
    skip: int = Query(0, ge=0, description="Number of records to skip"),
    limit: int = Query(100, ge=1, le=1000, description="Number of records to return")
) -> List[ShopItem]:
    """List all shop items with optional category filter and pagination"""
    query = select(ShopItem)
    
    if category_id:
        query = query.join(ShopItemCategoryAssociation).where(
            ShopItemCategoryAssociation.category_id == category_id
        )
    
    items = session.exec(query.offset(skip).limit(limit)).all()
    return items


@router.get("/{item_id}", response_model=ShopItemRead)
def get_shop_item(item_id: int, session: SessionDep) -> ShopItem:
    """Get a shop item by ID"""
    item = session.get(ShopItem, item_id)
    if not item:
        raise HTTPException(status_code=404, detail="Shop item not found")
    return item


@router.post("/", response_model=ShopItemRead, status_code=201)
def create_shop_item(item: ShopItemCreate, session: SessionDep) -> ShopItem:
    """Create a new shop item"""
    # Extract category IDs and create the shop item
    category_ids = item.category_ids or []
    item_data = item.model_dump(exclude={"category_ids"})
    
    # Create the shop item
    db_item = ShopItem(**item_data)
    session.add(db_item)
    session.commit()
    session.refresh(db_item)
    
    # Add categories to association table
    for category_id in category_ids:
        category = session.get(ShopItemCategory, category_id)
        if category:
            # Create association record
            association = ShopItemCategoryAssociation(
                shop_item_id=db_item.id,
                category_id=category_id
            )
            session.add(association)
    
    session.commit()
    session.refresh(db_item)
    return db_item


@router.put("/{item_id}", response_model=ShopItemRead)
def update_shop_item(
    item_id: int,
    item: ShopItemUpdate,
    session: SessionDep
) -> ShopItem:
    """Update a shop item"""
    db_item = session.get(ShopItem, item_id)
    if not db_item:
        raise HTTPException(status_code=404, detail="Shop item not found")
    
    # Extract category IDs
    category_ids = item.category_ids
    item_data = item.model_dump(exclude_unset=True, exclude={"category_ids"})
    
    # Update item fields
    for field, value in item_data.items():
        setattr(db_item, field, value)
    
    # Update categories if provided
    if category_ids is not None:
        # Delete existing associations
        existing_associations = session.exec(
            select(ShopItemCategoryAssociation).where(
                ShopItemCategoryAssociation.shop_item_id == item_id
            )
        ).all()
        for assoc in existing_associations:
            session.delete(assoc)
        
        # Create new associations
        for category_id in category_ids:
            category = session.get(ShopItemCategory, category_id)
            if category:
                association = ShopItemCategoryAssociation(
                    shop_item_id=item_id,
                    category_id=category_id
                )
                session.add(association)
    
    session.add(db_item)
    session.commit()
    session.refresh(db_item)
    return db_item


@router.delete("/{item_id}")
def delete_shop_item(item_id: int, session: SessionDep) -> dict:
    """Delete a shop item"""
    item = session.get(ShopItem, item_id)
    if not item:
        raise HTTPException(status_code=404, detail="Shop item not found")
    
    session.delete(item)
    session.commit()
    return {"message": "Shop item deleted successfully"}
