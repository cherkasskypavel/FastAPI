"""init_revision

Revision ID: 9d6550af8c67
Revises: 
Create Date: 2024-02-06 15:17:40.838052

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '9d6550af8c67'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        "users",
        sa.Column('id', sa.Integer, primary_key=True, autoincrement=True),
        sa.Column('email', sa.String, nullable=False, unique=True),
        sa.Column('hashed_password', sa.String, nullable=False),
        sa.Column('role', sa.String, server_default='user')
    )


    op.create_table(
        "posts",
        sa.Column('id', sa.Integer, primary_key=True, autoincrement=True),
        sa.Column('subject', sa.String, nullable=False),
        sa.Column('text', sa.String, nullable=False),
        sa.Column('author_id', sa.Integer, sa.ForeignKey('users.id')),
        sa.Column('post_time', sa.DateTime, nullable=False),
        sa.Column('is_edited', sa.Boolean, default=False),
        sa.Column('edited_by', sa.String, server_default=None)
    )


def downgrade() -> None:
    op.drop_table('users')
    op.drop_table('posts')
