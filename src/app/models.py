"""Expense model definition for the Expense Tracker API.

This module defines the Expense document model used with Beanie ODM for MongoDB.
"""

from beanie import Document
from pydantic import Field


class Expense(Document):
    """
    Expense document model for MongoDB.

    Attributes:
        name (str): Name of the expense.
        amount (float): Amount of the expense.
        category (str): Category of the expense.
    """

    name: str = Field(..., description="Name of the expense")
    amount: float = Field(..., description="Amount of the expense")
    category: str = Field(..., description="Category of the expense")

    class Settings:
        name = "expenses"  # Collection name
