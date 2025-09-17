from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session
from src.app.database.postgres import SessionLocal
from src.app.models.postgres import Budget, Category, Expense
from src.app.schema.postgres import BudgetIn, BudgetOut, CategoryOut, CategoryIn, ExpenseIn, ExpenseOut
from src.app.exceptions import NotFoundException

router = APIRouter(prefix="/api/v1/postgres")


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
        

@router.get(
    "/expenses",
    name="get_expenses",
    tags=["expenses"],
    status_code=status.HTTP_200_OK,
    response_model=list[ExpenseOut], 
    response_description="List of all expenses",
    summary="Get all expenses",
    description="Retrieve a list of all expenses stored in the database.",
)
async def get_expenses(db: Session = Depends(get_db)) -> list[ExpenseOut]:
    """
    Retrieve all expenses.

    Returns:
        List[Expense]: A list of all expense objects.
    """
    expenses = db.query(Expense).all()

    return expenses
    

@router.get(
    "/expenses/{expense_id}",
    name="get_expense",
    tags=["expenses"],
    status_code=status.HTTP_200_OK,
    # response_model=ExpenseOut,
    summary="Get a specific expense",
    description="Retrieve a specific expense by its unique ID.",
)
async def get_expense(expense_id: int , db: Session = Depends(get_db)):
    """
    Retrieve a specific expense by ID.

    Args:
        expense_id (id): The unique identifier of the expense.

    Returns:
        Expense: The expense object if found.

    Raises:
        HTTPException: If the expense is not found (404).
    """
    expense = db.query(Expense).filter(Expense.id == expense_id).first()
    print("EXPENSEEEE", expense)
    if not expense:
        raise NotFoundException({"message": "Expense not found", "code": 404})
    return expense


@router.post(
    "/expenses",
    name="create_expense",
    tags=["expenses"],
    status_code=status.HTTP_201_CREATED,
    response_model=ExpenseOut,
    summary="Create a new expense",
    description="Create and store a new expense in the database.",
)
async def create_expense(expense_in: ExpenseIn,db: Session = Depends(get_db)):
    """
    Create a new expense.

    Args:
        expense_in (ExpenseIn): The expense data to create.

    Returns:
        Expense: The created expense object.
    """
    expense = Expense(**expense_in.model_dump())
    db.add(expense)
    db.commit()
    db.refresh(expense)
    return expense
    
    

# @router.delete(
#     "/expenses/{expense_id}",
#     name="delete_expense",
#     tags=["expenses"],
#     status_code=status.HTTP_204_NO_CONTENT,
#     summary="Delete an expense",
#     description="Delete a specific expense by its unique ID."
# )
# async def delete_expense(expense_id: id, db: Session = Depends(get_db)):
#     """
#     Delete a specific expense by ID.

#     Args:
#         expense_id (id): The unique identifier of the expense.

#     Raises:
#         HTTPException: If the expense is not found (404).
#     """
#     expense = db.delete(Expense).filter(Expense.id == expense_id)
#     if not expense:
#         raise NotFoundException({"message": "Expense not found", "code": 404})
#     db.commit()
#     return 0
    
# @router.patch(
#     "/expenses/{expense_id}",
#     name="update_expense",
#     tags=["expenses"],
#     status_code=status.HTTP_200_OK,
#     response_model=Expense,
#     summary="Update an expense",
#     description="Update an existing expense by its unique ID."
# )
# async def update_expense(expense_id: id, expense_in: ExpenseIn, db: Session = Depends(get_db)):
#     """
#     Update an existing expense by ID.
#     Args:
#         expense_id (id): The unique identifier of the expense.
#         expense_in (ExpenseIn): The updated expense data.
#     Returns:
#         Expense: The updated expense object.
#     Raises:
#         HTTPException: If the expense is not found (404).
#     """
#     expense = db.query.Expense.filter(Expense.id == expense_id).first()
#     if not expense:
#         raise NotFoundException({"message": "Expense not found", "code": 404})
    
#     expense.name = expense_in.name
#     expense.amount = expense_in.amount
#     expense.category_id = expense_in.category
#     expense.budget_id = expense_in.budget
#     db.commit()
#     db.refresh(expense) 
#     return expense

@router.post(
    "/categories",
    name="create_category",
    tags=["categories"],
    status_code=status.HTTP_201_CREATED,
    response_model=CategoryOut,
    summary="Create a new category",
    description="Create and store a new category in the database."
)
async def create_category(category_in: CategoryIn, db: Session = Depends(get_db)):
    """
    Create a new category.

    Args:
        category_in (CategoryIn): The category data to create.

    Returns:
        Category: The created category object.
        
    """
    
    category = Category(**category_in.model_dump())
    db.add(category)
    db.commit()
    db.refresh(category)
    return category

@router.get(
    "/categories",
    name="get_categories",
    tags=["categories"],
    status_code=status.HTTP_200_OK,
    response_model=list[CategoryOut],
    summary="Get all categories",
    description="Retrieve a list of all categories stored in the database."
)
async def get_categories(db: Session = Depends(get_db)) :
    """
    Retrieve all categories.

    Returns:
        List[Category]: A list of all category objects.
    """
    categories = db.query(Category).all()
    return categories


@router.post(
    "/budgets",
    name="create_budget",
    tags=["budgets"],
    status_code=status.HTTP_201_CREATED,
    response_model=BudgetOut,
    summary="Create a new budget",
    description="Create and store a new budget in the database."
)
async def create_budget(budget_in: BudgetIn, db: Session = Depends(get_db)):
    """
    Create a new budget.

    Args:
        budget_in (BudgetIn): The budget data to create.

    Returns:
        Budget: The created budget object.
    """
    budget = Budget(**budget_in.model_dump())
    db.add(budget)
    db.commit()
    db.refresh(budget)
    return budget

@router.get(
    "/budgets",
    name="get_budgets",
    tags=["budgets"],
    status_code=status.HTTP_200_OK,
    response_model=list[BudgetOut],
    summary="Get all budgets",
    description="Retrieve a list of all budgets stored in the database."
)
async def get_budgets(db: Session = Depends(get_db)):
    """
    Retrieve all budgets.

    Returns:
        List[Budget]: A list of all budget objects.
    """
    budgets = db.query(Budget).all()
    return budgets

# @router.get(
#     "/budgets/{budget_id}",
#     name="get_budget",
#     tags=["budgets"],
#     status_code=status.HTTP_200_OK,
#     response_model=BudgetOut,
#     summary="Get a specific budget",
#     description="Retrieve a specific budget by its unique ID."  
#     )

# async def get_budget(budget_id: id, db: Session = Depends(get_db)):
#     """
#     Retrieve a specific budget by ID.

#     Args:
#         budget_id (id): The unique identifier of the budget.

#     Returns:
#         Budget: The budget object if found.

#     Raises:
#         HTTPException: If the budget is not found (404).
#     """
#     budget = db.query.Budget.filter(Budget.id == budget_id).first()
#     if not budget:
#         raise NotFoundException({"message": "Budget not found", "code": 404})
#     return budget

# @router.patch(
#     "/budgets/{budget_id}",
#     name="update_budget",
#     tags=["budgets"],
#     status_code=status.HTTP_200_OK,
#     response_model=Budget,
#     summary="Update a budget",
#     description="Update an existing budget by its unique ID."
# )
# async def update_budget(budget_id: id, budget_in: BudgetIn, db: Session = Depends(get_db)):
#     """
#     Update an existing budget by ID.

#     Args:
#         budget_id (id): The unique identifier of the budget.
#         budget_in (BudgetIn): The updated budget data.

#     Returns:
#         Budget: The updated budget object.

#     Raises:
#         HTTPException: If the budget is not found (404).
#     """
#     budget = db.query.Budget.filter(Budget.id == budget_id).first()
#     if not budget:
#         raise NotFoundException({"message": "Budget not found", "code": 404})   

    
#     budget.name = budget_in.name
#     budget.amount = budget_in.amount
#     db.commit()
#     db.refresh(budget)     
#     return budget