"""
Main FastAPI application
"""
from fastapi import FastAPI
from app.database import create_db_and_tables, get_session
from app.database.init_data import initialize_test_data
from app.routers import customers_router, categories_router, shop_items_router, orders_router


# Create FastAPI app
app = FastAPI(
    title="Online Shop API",
    description="A minimalistic backend web application for an online shop with full CRUD functionality",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc"
)


# Include routers
app.include_router(customers_router, prefix="/api/v1")
app.include_router(categories_router, prefix="/api/v1")
app.include_router(shop_items_router, prefix="/api/v1")
app.include_router(orders_router, prefix="/api/v1")


@app.on_event("startup")
def on_startup():
    """Initialize database and test data on startup"""
    create_db_and_tables()
    
    # Initialize test data
    with next(get_session()) as session:
        initialize_test_data(session)


@app.get("/")
def read_root():
    """Root endpoint"""
    return {
        "message": "Welcome to Online Shop API",
        "version": "1.0.0",
        "docs": "/docs",
        "redoc": "/redoc"
    }


@app.get("/health")
def health_check():
    """Health check endpoint"""
    return {"status": "healthy"}


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
