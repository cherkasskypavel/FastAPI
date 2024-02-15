"""initial

Revision ID: 4ef4da1c7c86
Revises: 
Create Date: 2024-02-04 15:21:02.572691

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa

from app.config import load_config

# revision identifiers, used by Alembic.
revision: str = '4ef4da1c7c86'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None

## подгоняем инициализацию alembic под уже существующую БД
## в консоли ввести:
## $ alembic stamp <№ ревизии>
def upgrade() -> None:
    dump_path = load_config().dump_path
    with open(dump_path, 'r') as dump_file:
        op.execute(sa.text(dump_file.read()))
    op.execute(sa.text("SET search_path = public"))


def downgrade() -> None:
    pass
