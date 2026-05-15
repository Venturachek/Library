"""add Loan

Revision ID: cb866ccae890
Revises: eb58248617f3
Create Date: 2026-05-10 20:14:18.549855

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa

revision: str = "cb866ccae890"
down_revision: Union[str, Sequence[str], None] = "eb58248617f3"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        "loan",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("user_id", sa.Integer(), nullable=False),
        sa.Column("book_id", sa.Integer(), nullable=False),
        sa.Column("loan_from", sa.Date(), nullable=False),
        sa.Column("loan_to", sa.Date(), nullable=False),
        sa.Column("returned", sa.Boolean(), nullable=False),
        sa.ForeignKeyConstraint(
            ["book_id"],
            ["book.id"],
        ),
        sa.ForeignKeyConstraint(
            ["user_id"],
            ["user.id"],
        ),
        sa.PrimaryKeyConstraint("id"),
    )



def downgrade() -> None:
    op.drop_table("loan")

