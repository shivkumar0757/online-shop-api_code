"""
Shop item and category data models
"""
from typing import Optional, List
from sqlmodel import SQLModel, Field


class CategoryBase(SQLModel):
    """Base category model with common fields"""
    title: str = Field(max_length=200, description="Category title")
    description: str = Field(description="Category description")


class ShopItemCategory(CategoryBase, table=True):
    """Shop item category database model"""
    __tablename__ = "shop_item_categories"
    
    id: Optional[int] = Field(default=None, primary_key=True, description="Category ID")


class CategoryCreate(CategoryBase):
    """Category creation model"""
    pass


class CategoryUpdate(CategoryBase):
    """Category update model - all fields optional"""
    title: Optional[str] = Field(default=None, max_length=200)
    description: Optional[str] = Field(default=None)


class CategoryRead(CategoryBase):
    """Category read model with ID"""
    id: int


class ShopItemCategoryAssociation(SQLModel, table=True):
    """Association table for many-to-many relationship between shop items and categories"""
    __tablename__ = "shop_item_category_association"
    
    shop_item_id: Optional[int] = Field(default=None, foreign_key="shop_items.id", primary_key=True)
    category_id: Optional[int] = Field(default=None, foreign_key="shop_item_categories.id", primary_key=True)


class ShopItemBase(SQLModel):
    """Base shop item model with common fields"""
    title: str = Field(max_length=200, description="Item title")
    description: str = Field(description="Item description")
    price: float = Field(gt=0, description="Item price (must be positive)")


class ShopItem(ShopItemBase, table=True):
    """Shop item database model"""
    __tablename__ = "shop_items"
    
    id: Optional[int] = Field(default=None, primary_key=True, description="Item ID")


class ShopItemCreate(ShopItemBase):
    """Shop item creation model"""
    category_ids: Optional[List[int]] = Field(default=[], description="List of category IDs")


class ShopItemUpdate(ShopItemBase):
    """Shop item update model - all fields optional"""
    title: Optional[str] = Field(default=None, max_length=200)
    description: Optional[str] = Field(default=None)
    price: Optional[float] = Field(default=None, gt=0)
    category_ids: Optional[List[int]] = Field(default=None, description="List of category IDs")


class ShopItemRead(ShopItemBase):
    """Shop item read model with ID and categories"""
    id: int
    categories: List[CategoryRead] = []
