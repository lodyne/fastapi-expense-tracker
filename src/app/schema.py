"""Pydantic schemas for the Expense Tracker API.

This module defines input validation schemas for expenses.
"""

from pydantic import BaseModel, Field


class ExpenseIn(BaseModel):
    """
    Schema for creating a new expense.

    Attributes:
        name (str): Name of the expense.
        amount (float): Amount of the expense.
        category (str): Category of the expense.
    """

    name: str = Field(..., description="Name of the expense")
    amount: float = Field(..., description="Amount of the expense")
    category: str = Field(..., description="Category of the expense")
