from fastapi import HTTPException
from sqlalchemy.orm import Session

from src.app.models.expense import Expense

def get_all_expenses(db: Session):
    """Retrieve all budgets from the database.

    Args:
        db (Session): SQLAlchemy database session.  
    Returns:
        List[Expense]: A list of all Budget objects.     
        
    """
    all_expenses = db.query(Expense).all()
    return all_expenses

def get_specific_expense(db: Session, expense_id: int):
    """Retrieve a specific expense by its ID.

    Args:
        db (Session): SQLAlchemy database session.
        expense_id (int): The ID of the expense to retrieve.

    Returns:
        Expense: The Expense object with the specified ID, or None if not found.
    """
    specific_expense = db.query(Expense).filter(Expense.id == expense_id).first()
    if not specific_expense:
        raise HTTPException(
            status_code=404,
            detail={"message": "Expense not found", "code": 404},
        )
    return specific_expense

def create_expense(expense: Expense, db: Session):
    """Create a new expense in the database.

    Args:
        expense (Expense): The Expense object to create.
        db (Session): SQLAlchemy database session.

    Returns:
        Expense: The newly created Expense object.
    """
    if expense is None:
        raise HTTPException(status_code=400, detail="Expense payload is required")
    db.add(expense)
    db.commit()
    db.refresh(expense)
    return expense
