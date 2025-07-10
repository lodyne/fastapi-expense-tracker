"""Pydantic schemas for the Expense Tracker API.

This module defines input validation schemas for expenses.
"""

from beanie import PydanticObjectId
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
    category: PydanticObjectId = Field(..., description="Category of the expense")
    budget: PydanticObjectId | None = Field(
        None, description="Budget associated with the expense"
    )

class CategoryIn(BaseModel):
    """
    Schema for creating a new category.

    Attributes:
        name (str): Name of the category.
    """

    name: str = Field(..., description="Name of the category")

class BudgetIn(BaseModel):
    """
    Schema for creating a new budget.

    Attributes:
        name (str): Name of the budget.
        amount (float): Total amount allocated for the budget.
    """

    name: str = Field(..., description="Name of the budget")
    amount: float = Field(..., description="Total amount allocated for the budget")

class CategoryOut(BaseModel):

    name: str

class BudgetOut(BaseModel):
    name: str
    amount: float

class ExpenseOut(BaseModel):
    name: str
    amount: float
    category: CategoryOut
    budget: BudgetOut