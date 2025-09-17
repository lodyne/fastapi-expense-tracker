"""Main entry point for the Expense Tracker API.

This module initializes the FastAPI application, sets up the application
lifespan for database initialization, and includes the API routes.
"""

from fastapi import FastAPI
from contextlib import asynccontextmanager
from src.app.database.mongo import init_db
from src.app.routes.mongo import router as mongo_router
# from src.app.routes.postgres import router as postgres_router

from src.app.utils import cors_config

@asynccontextmanager
async def lifespan(app: FastAPI):
    """
    Application lifespan context manager.

    Initializes the database connection when the application starts.
    """
    await init_db()
    yield


app = FastAPI(
    title="Expense Tracker API",
    description="An API for tracking expenses and managing budgets",
    version="1.0.0",
    contact={"name": "Lodger Mtui", "email": "lodgmtui@gmail.com"},
    license_info={"name": "MIT License", "url": "https://opensource.org/license/mit/"},
    openapi_tags=[
        {"name": "expenses", "description": "Operations related to expenses"},
        {"name": "categories", "description": "Operations related to categories"},
        {"name": "budgets", "description": "Operations related to budgets"},
    ],
    lifespan=lifespan,
    docs_url="/docs",
    redoc_url="/redoc",
    openapi_url="/openapi.json",
    debug=True,
    title_format="{title} - {version}",
    description_format="{description} - {contact[name]} ({contact[email]})",
)

cors_config(app)  # Configure CORS settings

@app.get("/")
async def root():
    """
    Root endpoint for the API.

    Returns:
        dict: A welcome message.
    """
    return {"message": "Hello, World!"}


app.include_router(mongo_router)
# app.include_router(postgres_router)
