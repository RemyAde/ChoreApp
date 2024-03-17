"""create apt_num for address col

Revision ID: 3087da7624f6
Revises: 2018bd1dd014
Create Date: 2024-03-17 00:45:03.932534

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '3087da7624f6'
down_revision: Union[str, None] = '2018bd1dd014'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column("address", sa.Column("apt_num", sa.Integer(), nullable=True))


def downgrade() -> None:
    op.drop_column("address", "apt_num")
