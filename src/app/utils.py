from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

def cors_config(app: FastAPI):
    """
    Configure CORS settings for the FastAPI application.

    Args:
        app (FastAPI): The FastAPI application instance.
    """
    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],  # Allow all origins for CORS
        allow_credentials=True,
        allow_methods=["*"],  # Allow all methods for CORS
        allow_headers=["*"],  # Allow all headers for CORS
    )