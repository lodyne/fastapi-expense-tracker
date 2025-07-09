from beanie import PydanticObjectId
from fastapi import APIRouter, HTTPException

from app.models import Expense
from app.schema import ExpenseIn

router = APIRouter()


@router.get(
    "/expenses",
    response_model=list[Expense],
    summary="Get all expenses",
    description="Retrieve a list of all expenses stored in the database.",
)
async def get_expenses():
    """
    Retrieve all expenses.

    Returns:
        List[Expense]: A list of all expense objects.
    """
    expenses = await Expense.find_all().to_list()
    return expenses


@router.get(
    "/expenses/{expense_id}",
    response_model=Expense,
    summary="Get a specific expense",
    description="Retrieve a specific expense by its unique ID.",
)
async def get_expense(expense_id: PydanticObjectId):
    """
    Retrieve a specific expense by ID.

    Args:
        expense_id (PydanticObjectId): The unique identifier of the expense.

    Returns:
        Expense: The expense object if found.

    Raises:
        HTTPException: If the expense is not found (404).
    """
    expense = await Expense.get(expense_id)
    if not expense:
        raise HTTPException(status_code=404, detail="Expense not found")
    return expense


@router.post(
    "/expenses",
    response_model=Expense,
    summary="Create a new expense",
    description="Create and store a new expense in the database.",
)
async def create_expense(expense_in: ExpenseIn):
    """
    Create a new expense.

    Args:
        expense_in (ExpenseIn): The expense data to create.

    Returns:
        Expense: The created expense object.
    """
    expense = Expense(**expense_in.dict())
    await expense.insert()
    return expense
