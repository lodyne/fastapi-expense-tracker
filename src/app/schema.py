"""Pydantic schemas for the Expense Tracker API.

This module defines input validation schemas for expenses.
"""

from typing import Optional
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
    """
    Schema for returning category information.

    Attributes:
        name (str): Name of the category.
    """
    id: PydanticObjectId
    name: str
    
    class Config:
        """
        Pydantic configuration for the CategoryOut model.
        
        Allows the use of alias for the _id field.
        """
        validate_by_name = True

class BudgetOut(BaseModel):
    """
    Schema for returning budget information.

    Attributes:
        name (str): Name of the budget.
        amount (float): Total amount allocated for the budget.
    """
    id: PydanticObjectId
    name: str
    amount: float
    
    class Config:
        """
        Pydantic configuration for the BudgetOut model.
        
        Allows the use of alias for the _id field.
        """
        validate_by_name = True

class ExpenseOut(BaseModel):
    """
    Schema for returning expense information with embedded category and budget.

    Attributes:
        name (str): Name of the expense.
        amount (float): Amount of the expense.
        category (CategoryOut): Category the expense belongs to.
        budget (BudgetOut): Budget the expense is associated with.
    """
    id: PydanticObjectId
    name: str
    amount: float
    category: Optional[CategoryOut]
    budget: Optional[BudgetOut]
    
    class Config:
        """
        Pydantic configuration for the ExpenseOut model.
        
        Allows the use of alias for the _id field.
        """
        validate_by_name = True
    


class ExpenseUpdate(BaseModel):
    """Schema for updating an existing expense.     
    Attributes:
        name (str, optional): Name of the expense.
        amount (float, optional): Amount of the expense.
        category (PydanticObjectId, optional): Category of the expense.
        budget (PydanticObjectId, optional): Budget associated with the expense.
    """
    name: Optional[str] = None
    amount: Optional[float] = None
    category: Optional[PydanticObjectId] = None
    budget: Optional[PydanticObjectId] = None