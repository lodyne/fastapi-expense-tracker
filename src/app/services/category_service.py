from fastapi import HTTPException
from src.app.models.expense import Category
from sqlalchemy.orm import Session


def get_all_categories(db: Session):
    all_categories = db.query(Category).all()
    return all_categories

def get_specific_category(category_id: int, db: Session):
    specific_category = db.query(Category).filter(Category.id == category_id).first()
    if not specific_category:
        raise HTTPException(status_code=404, detail="Category not found")
    return specific_category


def create_category(category:Category, db: Session):
    if category is None:
        raise HTTPException(status_code=400, detail="Category payload is required")
    db.add(category)
    db.commit()
    db.refresh(category)
    return category
