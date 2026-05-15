"""Add Loan

Revision ID: eb58248617f3
Revises: 82efe4f593cc
Create Date: 2026-05-10 20:13:27.020792

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa

revision: str = "eb58248617f3"
down_revision: Union[str, Sequence[str], None] = "82efe4f593cc"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        "user",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("email", sa.String(length=200), nullable=False),
        sa.Column("hashed_password", sa.String(length=200), nullable=False),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("email"),
    )

def downgrade() -> None:
    op.drop_table("user")

