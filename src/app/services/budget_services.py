from fastapi import HTTPException
from sqlalchemy.orm import Session

from src.app.models.expense import Budget


def get_all_budgets(db:Session):
    """Retrieve all budgets from the database.

    Args:
        db (Session): SQLAlchemy database session.  
    Returns:
        List[Budget]: A list of all Budget objects.     
        
    """
    all_budgets = db.query(Budget).all()
    return all_budgets

def get_specific_budget(db:Session, budget_id:int):
    """Retrieve a specific budget by its ID.

    Args:
        db (Session): SQLAlchemy database session.
        budget_id (int): The ID of the budget to retrieve.

    Returns:
        Budget: The Budget object with the specified ID, or None if not found.
    """
    specific_budget = db.query(Budget).filter(Budget.id == budget_id).first()
    if not specific_budget:
        raise HTTPException({"message": "Budget not found", "code": 404})
    return specific_budget


def create_budget(budget:Budget, db:Session):
    """Create a new budget in the database.

    Args:
        budget (Budget): The Budget object to create.
        db (Session): SQLAlchemy database session.

    Returns:
        Budget: The newly created Budget object.
    """
    if budget is None:
        raise HTTPException(status_code=400, detail="Budget payload is required")
    db.add(budget)
    db.commit()
    db.refresh(budget)
    return budget