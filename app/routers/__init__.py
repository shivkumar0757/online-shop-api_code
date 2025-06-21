"""
Routers package initialization
"""
from .customers import router as customers_router
from .categories import router as categories_router
from .shop_items import router as shop_items_router
from .orders import router as orders_router

__all__ = ["customers_router", "categories_router", "shop_items_router", "orders_router"]
