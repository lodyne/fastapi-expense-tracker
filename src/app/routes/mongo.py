from beanie import PydanticObjectId
from fastapi import APIRouter, HTTPException, status

from src.app.models.mongo import Budget, Category, Expense, Income
from src.app.schema.mongodb import BudgetIn, BudgetOut, CategoryIn, CategoryOut, ExpenseIn, ExpenseOut, IncomeIn, IncomeOut
from src.app.exceptions import NotFoundException

router = APIRouter(prefix="/api/v1/mongo")

@router.get(
    "/income/{income_id}",
    name="get_income",
    tags = ["income - mongo"],
    status_code=status.HTTP_200_OK,
    response_model=IncomeOut,
    response_description="The created income",
    summary="Get the income",
    description="Retrieve the created income"
)

async def get_income(income_id: PydanticObjectId):
    income = await Income.get(income_id, fetch_links = True)
    if not income:
        raise NotFoundException({"message": "Expense not found", "code": 404})
    return income

@router.post(
    "/income",
    name="create_income",
    tags=["income - mongo"],
    status_code=status.HTTP_201_CREATED,
    response_model=IncomeOut,
    summary="Create a new income",
    description="Create and store a new income in the database."
)
async def create_income(income_in: IncomeIn):
    """
    Create a new income.

    Args:
        income (IncomeIn): The income data to create.

    Returns:
        Budget: The created income object.
    """
    income = Income(**income_in.model_dump())
    await income.insert()
    return income

@router.get(
    "/expenses",
    name="get_expenses",
    tags=["expenses - mongo"],
    status_code=status.HTTP_200_OK,
    response_model=list[ExpenseOut], 
    response_description="List of all expenses",
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
    tags=["expenses - mongo"],
    status_code=status.HTTP_200_OK,
    response_model=ExpenseOut,
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
    expense = await Expense.get(expense_id, fetch_links=True)
    if not expense:
        raise NotFoundException({"message": "Expense not found", "code": 404})
    return expense


@router.post(
    "/expenses",
    name="create_expense",
    tags=["expenses - mongo"],
    status_code=status.HTTP_201_CREATED,
    response_model=ExpenseOut,
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

    # Resolve linked category and budget
    category = await expense.category.fetch()
    budget = await expense.budget.fetch() if expense.budget else None

    # Return formatted response
    return ExpenseOut(
        id=expense.id,
        name=expense.name,
        amount=expense.amount,
        category=CategoryOut(
            id=category.id,
            name=category.name
        ) if category else None,
        budget=BudgetOut(
            id=budget.id,
            name=budget.name,
            amount=budget.amount
        ) if budget else None,
    )
    

@router.delete(
    "/expenses/{expense_id}",
    name="delete_expense",
    tags=["expenses - mongo"],
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
    
@router.patch(
    "/expenses/{expense_id}",
    name="update_expense",
    tags=["expenses - mongo"],
    status_code=status.HTTP_200_OK,
    response_model=Expense,
    summary="Update an expense",
    description="Update an existing expense by its unique ID."
)
async def update_expense(expense_id: PydanticObjectId, expense_in: ExpenseIn):
    """
    Update an existing expense by ID.
    Args:
        expense_id (PydanticObjectId): The unique identifier of the expense.
        expense_in (ExpenseIn): The updated expense data.
    Returns:
        Expense: The updated expense object.
    Raises:
        HTTPException: If the expense is not found (404).
    """
    expense = await Expense.get(expense_id)
    if not expense:
        raise HTTPException(status_code=404, detail="Expense not found")
    
    expense.name = expense_in.name
    expense.amount = expense_in.amount
    expense.category = expense_in.category
    expense.budget = expense_in.budget
    await expense.save()
    
    return expense

@router.post(
    "/categories",
    name="create_category",
    tags=["categories - mongo"],
    status_code=status.HTTP_201_CREATED,
    response_model=CategoryOut,
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
    tags=["categories - mongo"],
    status_code=status.HTTP_200_OK,
    response_model=list[CategoryOut],
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


@router.get(
    "/categories/{category_id}",
    name="get_category",
    tags = ["categories - mongo"],
    status_code=status.HTTP_200_OK,
    response_model=CategoryOut,
    response_description="The specific category",
    summary="Get the category",
    description="Retrieve the specific category"
)
async def get_category(category_id: PydanticObjectId):
    category = await Category.get(category_id)
    if not category:
        raise NotFoundException({"message": "Category not found", "code": 404})
    return category


@router.post(
    "/budgets",
    name="create_budget",
    tags=["budgets - mongo"],
    status_code=status.HTTP_201_CREATED,
    response_model=BudgetOut,
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
    tags=["budgets - mongo"],
    status_code=status.HTTP_200_OK,
    response_model=list[BudgetOut],
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

@router.get(
    "/budgets/{budget_id}",
    name="get_budget",
    tags=["budgets - mongo"],
    status_code=status.HTTP_200_OK,
    response_model=BudgetOut,
    summary="Get a specific budget",
    description="Retrieve a specific budget by its unique ID."  
    )

async def get_budget(budget_id: PydanticObjectId):
    """
    Retrieve a specific budget by ID.

    Args:
        budget_id (PydanticObjectId): The unique identifier of the budget.

    Returns:
        Budget: The budget object if found.

    Raises:
        HTTPException: If the budget is not found (404).
    """
    budget = await Budget.get(budget_id)
    if not budget:
        raise HTTPException(status_code=404, detail="Budget not found")
    return budget

@router.patch(
    "/budgets/{budget_id}",
    name="update_budget",
    tags=["budgets - mongo"],
    status_code=status.HTTP_200_OK,
    response_model=BudgetOut,
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