# """Database configuration and initialization for the Expense Tracker API.

# This module sets up the MongoDB connection using Motor and initializes
# the Beanie ODM with the Expense document model.
# """

# from beanie import init_beanie
# import logging
# from motor.motor_asyncio import AsyncIOMotorClient
# from dotenv import load_dotenv
# import os

# from src.app.models.mongo import Budget, Category, Expense, Income

# # Load environment variables from .env file
# load_dotenv()  # Loads variables from .env into environment

# # Retrieve MongoDB configuration from environment variables
# MONGO_URL = os.getenv("MONGO_URL")
# MONGO_DB_NAME = os.getenv("MONGO_DB_NAME")
# MONGO_COLLECTION_NAME = os.getenv("MONGO_COLLECTION_NAME")

# # Validate required environment variables
# if not MONGO_URL:
#     raise ValueError("MONGO_URL environment variable is required")
# if not MONGO_DB_NAME:
#     raise ValueError("MONGO_DB_NAME environment variable is required")

# # Initialize MongoDB client and database references

# client = AsyncIOMotorClient(MONGO_URL)
# database = client[MONGO_DB_NAME]
# # expenses_collection = database[MONGO_COLLECTION_NAME]

# # Set up logger for this module
# logger = logging.getLogger(__name__)


# async def init_db():
#     """
#     Initialize the database connection and Beanie ODM.

#     This function connects to the MongoDB database and initializes Beanie
#     with the Expense document model. It should be called during application startup.
#     """
#     logger.info("Initializing database connection...")
#     await init_beanie(
#         database=database, document_models=[Expense, Category, Budget, Income]
#     )
#     logger.info("Database initialized successfully.")
