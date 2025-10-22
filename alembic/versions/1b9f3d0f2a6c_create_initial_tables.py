"""create initial tables for expense tracker

Revision ID: 1b9f3d0f2a6c
Revises:
Create Date: 2025-01-16 00:00:00.000000

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = "1b9f3d0f2a6c"
down_revision: Union[str, Sequence[str], None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Create core tables."""
    op.create_table(
        "categories",
        sa.Column("id", sa.Integer(), primary_key=True, autoincrement=True),
        sa.Column("name", sa.String(), nullable=False),
        sa.UniqueConstraint("name", name="uq_categories_name"),
    )
    op.create_index("ix_categories_id", "categories", ["id"], unique=True)
    op.create_index("ix_categories_name", "categories", ["name"], unique=True)

    op.create_table(
        "budgets",
        sa.Column("id", sa.Integer(), primary_key=True, autoincrement=True),
        sa.Column("name", sa.String(), nullable=False),
        sa.Column("amount", sa.Numeric(10, 2), nullable=False),
        sa.UniqueConstraint("name", name="uq_budgets_name"),
    )
    op.create_index("ix_budgets_id", "budgets", ["id"], unique=True)
    op.create_index("ix_budgets_name", "budgets", ["name"], unique=True)

    op.create_table(
        "expenses",
        sa.Column("id", sa.Integer(), primary_key=True, autoincrement=True),
        sa.Column("name", sa.String(), nullable=False),
        sa.Column("amount", sa.Numeric(10, 2), nullable=False),
        sa.Column("category_id", sa.Integer(), nullable=False),
        sa.Column("budget_id", sa.Integer(), nullable=True),
        sa.ForeignKeyConstraint(["category_id"], ["categories.id"]),
        sa.ForeignKeyConstraint(["budget_id"], ["budgets.id"]),
    )
    op.create_index("ix_expenses_id", "expenses", ["id"], unique=True)
    op.create_index("ix_expenses_name", "expenses", ["name"])


def downgrade() -> None:
    """Drop core tables."""
    op.drop_index("ix_expenses_name", table_name="expenses")
    op.drop_index("ix_expenses_id", table_name="expenses")
    op.drop_table("expenses")

    op.drop_index("ix_budgets_name", table_name="budgets")
    op.drop_index("ix_budgets_id", table_name="budgets")
    op.drop_table("budgets")

    op.drop_index("ix_categories_name", table_name="categories")
    op.drop_index("ix_categories_id", table_name="categories")
    op.drop_table("categories")
