"""Change User table

Revision ID: 78bf377b5207
Revises: 46e99ff14a22
Create Date: 2024-01-13 03:01:16.586190

"""
from typing import Sequence, Union

import sqlalchemy as sa

from alembic import op

# revision identifiers, used by Alembic.
revision: str = "78bf377b5207"
down_revision: Union[str, None] = "46e99ff14a22"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column("user", sa.Column("hashed_password", sa.String(), nullable=False))
    op.drop_column("user", "hash_password")
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column(
        "user",
        sa.Column("hash_password", sa.VARCHAR(), autoincrement=False, nullable=False),
    )
    op.drop_column("user", "hashed_password")
    # ### end Alembic commands ###