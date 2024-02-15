"""add column 'karma' to users table

Revision ID: 3a9f345f74c7
Revises: 4ef4da1c7c86
Create Date: 2024-02-08 19:49:14.908833

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision: str = '3a9f345f74c7'
down_revision: Union[str, None] = '4ef4da1c7c86'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column('users', sa.Column(
        'karma', sa.Integer, server_default='100'))
    op.execute("UPDATE users SET karma = 100")


def downgrade() -> None:
    op.drop_column('users', 'karma')