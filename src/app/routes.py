from beanie import PydanticObjectId
from fastapi import APIRouter, HTTPException, status

from app.models import Budget, Category, Expense
from app.schema import BudgetIn, CategoryIn, ExpenseIn, ExpenseOut

router = APIRouter()


@router.get(
    "/expenses",
    name="get_expenses",
    tags=["expenses"],
    status_code=status.HTTP_200_OK,
    response_model=list[ExpenseOut],
    summary="Get all expenses",
    description="Retrieve a list of all expenses stored in the database.",
)
async def get_expenses():
    """
    Retrieve all expenses.

    Returns:
        List[Expense]: A list of all expense objects.
    """
    expenses = await Expense.find_all(fetch_links=True).to_list()
    return expenses


@router.get(
    "/expenses/{expense_id}",
    name="get_expense",
    tags=["expenses"],
    status_code=status.HTTP_200_OK,
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
    name="create_expense",
    tags=["expenses"],
    status_code=status.HTTP_201_CREATED,
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
    expense = Expense(**expense_in.model_dump())
    await expense.insert()
    return expense

@router.post(
    "/categories",
    name="create_category",
    tags=["categories"],
    status_code=status.HTTP_201_CREATED,
    response_model=Category,
    summary="Create a new category",
    description="Create and store a new category in the database."
)
async def create_category(category_in: CategoryIn):
    """
    Create a new category.

    Args:
        category_in (CategoryIn): The category data to create.

    Returns:
        Category: The created category object.
    """
    category = Category(**category_in.model_dump())
    await category.insert()
    return category

@router.get(
    "/categories",
    name="get_categories",
    tags=["categories"],
    status_code=status.HTTP_200_OK,
    response_model=list[Category],
    summary="Get all categories",
    description="Retrieve a list of all categories stored in the database."
)
async def get_categories():
    """
    Retrieve all categories.

    Returns:
        List[Category]: A list of all category objects.
    """
    categories = await Category.find_all().to_list()
    return categories

@router.delete(
    "/expenses/{expense_id}",
    name="delete_expense",
    tags=["expenses"],
    status_code=status.HTTP_204_NO_CONTENT,
    summary="Delete an expense",
    description="Delete a specific expense by its unique ID."
)
async def delete_expense(expense_id: PydanticObjectId):
    """
    Delete a specific expense by ID.

    Args:
        expense_id (PydanticObjectId): The unique identifier of the expense.

    Raises:
        HTTPException: If the expense is not found (404).
    """
    expense = await Expense.get(expense_id)
    if not expense:
        raise HTTPException(status_code=404, detail="Expense not found")
    await expense.delete()

@router.post(
    "/budgets",
    name="create_budget",
    tags=["budgets"],
    status_code=status.HTTP_201_CREATED,
    response_model=Budget,
    summary="Create a new budget",
    description="Create and store a new budget in the database."
)
async def create_budget(budget_in: BudgetIn):
    """
    Create a new budget.

    Args:
        budget_in (BudgetIn): The budget data to create.

    Returns:
        Budget: The created budget object.
    """
    budget = Budget(**budget_in.model_dump())
    await budget.insert()
    return budget

@router.get(
    "/budgets",
    name="get_budgets",
    tags=["budgets"],
    status_code=status.HTTP_200_OK,
    response_model=list[Budget],
    summary="Get all budgets",
    description="Retrieve a list of all budgets stored in the database."
)
async def get_budgets():
    """
    Retrieve all budgets.

    Returns:
        List[Budget]: A list of all budget objects.
    """
    budgets = await Budget.find_all().to_list()
    return budgets

@router.patch(
    "/budgets/{budget_id}",
    name="update_budget",
    tags=["budgets"],
    status_code=status.HTTP_200_OK,
    response_model=Budget,
    summary="Update a budget",
    description="Update an existing budget by its unique ID."
)
async def update_budget(budget_id: PydanticObjectId, budget_in: BudgetIn):
    """
    Update an existing budget by ID.

    Args:
        budget_id (PydanticObjectId): The unique identifier of the budget.
        budget_in (BudgetIn): The updated budget data.

    Returns:
        Budget: The updated budget object.

    Raises:
        HTTPException: If the budget is not found (404).
    """
    budget = await Budget.get(budget_id)
    if not budget:
        raise HTTPException(status_code=404, detail="Budget not found")
    
    budget.name = budget_in.name
    budget.amount = budget_in.amount
    await budget.save()
    
    return budget