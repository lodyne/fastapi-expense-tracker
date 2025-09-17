from sqlalchemy import Column, Double,ForeignKey,Integer,String

from sqlalchemy.orm import relationship
from src.app.database.postgres import Base, engine

Base.metadata.create_all(bind=engine)


class Category(Base):
    __tablename__ = "categories"
    
    id = Column(Integer, primary_key = True, index = True, autoincrement=True)
    name = Column(String, unique = True, index = True, nullable = False)
    expenses = relationship("Expense", back_populates="category")
    
class Budget(Base):
    __tablename__ = "budgets"
    
    id = Column(Integer, primary_key = True, index = True, autoincrement=True)
    name = Column(String, unique = True, index= True, nullable=False)
    amount = Column(Double, nullable=False)
    expenses = relationship("Expense", back_populates="budget")
    
class Expense(Base):
    __tablename__ = "expenses"
    
    id = Column(Integer, primary_key = True, index = True, autoincrement=True)
    name = Column(String, index = True, nullable = False)
    amount = Column(Double, nullable = False)
    category_id = Column(Integer, ForeignKey("categories.id"), nullable = False)
    budget_id = Column(Integer, ForeignKey("budgets.id"), nullable = True)
    
    category = relationship("Category")
    budget = relationship("Budget")