from sqlalchemy import Column, ForeignKey, Integer, Numeric, String

from sqlalchemy.orm import relationship
from src.app.database.expense import Base, engine


def create_tables():
    Base.metadata.create_all(bind=engine)


class Category(Base):
    __tablename__ = "categories"

    id = Column(Integer, primary_key=True, index=True, unique=True, autoincrement=True)
    name = Column(String, unique=True, index=True, nullable=False)
    expenses = relationship("Expense", back_populates="category")


class Budget(Base):
    __tablename__ = "budgets"


    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    name = Column(String, unique=True, index=True, nullable=False)
    amount = Column(Numeric(10, 2), nullable=False)  # 10 digits, 2 decimal places
    expenses = relationship("Expense", back_populates="budget")


class Expense(Base):
    __tablename__ = "expenses"

    id = Column(Integer, primary_key=True, index=True, unique=True, autoincrement=True)
    name = Column(String, index=True, nullable=False)
    amount = Column(Numeric(10, 2), nullable=False)
    category_id = Column(Integer, ForeignKey("categories.id"), nullable=False)
    budget_id = Column(Integer, ForeignKey("budgets.id"), nullable=True)

    category = relationship("Category")
    budget = relationship("Budget")
