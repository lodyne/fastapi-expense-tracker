"""Expense model definition for the Expense Tracker API.

This module defines the Expense document model used with Beanie ODM for MongoDB.
"""

from beanie import Document, Link
from pydantic import Field


class Category(Document):
    """
    Category document model for MongoDB.

    Attributes:
        name (str): Name of the category.
    """

    name: str = Field(..., description="Name of the category")

    class Settings:
        name = "categories"  # Collection name
        

class Budget(Document):
    """
    Budget document model for MongoDB.

    Attributes:
        name (str): Name of the budget.
        amount (float): Total amount allocated for the budget.
    """

    name: str = Field(..., description="Name of the budget")
    amount: float = Field(..., description="Total amount allocated for the budget")

    class Settings:
        name = "budgets"  # Collection name
        
class Expense(Document):
    """
    Expense document model for MongoDB.

    Attributes:
        name (str): Name of the expense.
        amount (float): Amount of the expense.
        category (str): Category of the expense.
        budget (str, optional): Budget associated with the expense.
    """

    name: str = Field(..., description="Name of the expense")
    amount: float = Field(..., description="Amount of the expense")
    category: Link[Category] = Field(..., description="Category of the expense")
    budget: Link[Budget] = Field(None, description="Budget associated with the expense")

    class Settings:
        name = "expenses"  # Collection name