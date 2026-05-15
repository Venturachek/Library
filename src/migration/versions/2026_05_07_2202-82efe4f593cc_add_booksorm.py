"""add BooksOrm

Revision ID: 82efe4f593cc
Revises:
Create Date: 2026-05-07 22:02:24.315617

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision: str = "82efe4f593cc"
down_revision: Union[str, Sequence[str], None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        "book",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("title", sa.String(length=100), nullable=False),
        sa.Column("author", sa.String(length=100), nullable=False),
        sa.Column(
            "genre",
            sa.Enum(
                "FICTION", "NON_FICTION", "SCIENCE", "DETECTIVE", "HORROR", name="genre"
            ),
            nullable=False,
        ),
        sa.Column("price", sa.Integer(), nullable=False),
        sa.Column(
            "availability", sa.Boolean(), server_default=sa.text("true"), nullable=False
        ),
        sa.Column("available_from", sa.DateTime(), nullable=True),
        sa.PrimaryKeyConstraint("id"),
    )



def downgrade() -> None:
    op.drop_table("book")