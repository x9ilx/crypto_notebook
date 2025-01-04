"""Добавил ключ уникальности полей с названием монеты и айди пользователя.

Revision ID: 0e22bc0569bc
Revises: 92af03c4f28e
Create Date: 2025-01-04 12:55:54.652753

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '0e22bc0569bc'
down_revision: Union[str, None] = 'f23f3019ad6a'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('currency', schema=None) as batch_op:
        batch_op.create_unique_constraint('name_user_id_unique', ['name', 'user_id'])

    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('currency', schema=None) as batch_op:
        batch_op.drop_constraint('name_user_id_unique', type_='unique')

    # ### end Alembic commands ###
