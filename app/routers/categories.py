"""
Category CRUD endpoints
"""
from typing import List
from fastapi import APIRouter, HTTPException, Query
from sqlmodel import select
from app.database import SessionDep
from app.models import ShopItemCategory, CategoryCreate, CategoryUpdate, CategoryRead


router = APIRouter(prefix="/categories", tags=["categories"])


@router.get("/", response_model=List[CategoryRead])
def list_categories(
    session: SessionDep,
    skip: int = Query(0, ge=0, description="Number of records to skip"),
    limit: int = Query(100, ge=1, le=1000, description="Number of records to return")
) -> List[ShopItemCategory]:
    """List all categories with pagination"""
    categories = session.exec(select(ShopItemCategory).offset(skip).limit(limit)).all()
    return categories


@router.get("/{category_id}", response_model=CategoryRead)
def get_category(category_id: int, session: SessionDep) -> ShopItemCategory:
    """Get a category by ID"""
    category = session.get(ShopItemCategory, category_id)
    if not category:
        raise HTTPException(status_code=404, detail="Category not found")
    return category


@router.post("/", response_model=CategoryRead, status_code=201)
def create_category(category: CategoryCreate, session: SessionDep) -> ShopItemCategory:
    """Create a new category"""
    db_category = ShopItemCategory.model_validate(category)
    session.add(db_category)
    session.commit()
    session.refresh(db_category)
    return db_category


@router.put("/{category_id}", response_model=CategoryRead)
def update_category(
    category_id: int,
    category: CategoryUpdate,
    session: SessionDep
) -> ShopItemCategory:
    """Update a category"""
    db_category = session.get(ShopItemCategory, category_id)
    if not db_category:
        raise HTTPException(status_code=404, detail="Category not found")
    
    category_data = category.model_dump(exclude_unset=True)
    for field, value in category_data.items():
        setattr(db_category, field, value)
    
    session.add(db_category)
    session.commit()
    session.refresh(db_category)
    return db_category


@router.delete("/{category_id}")
def delete_category(category_id: int, session: SessionDep) -> dict:
    """Delete a category"""
    category = session.get(ShopItemCategory, category_id)
    if not category:
        raise HTTPException(status_code=404, detail="Category not found")
    
    session.delete(category)
    session.commit()
    return {"message": "Category deleted successfully"}
