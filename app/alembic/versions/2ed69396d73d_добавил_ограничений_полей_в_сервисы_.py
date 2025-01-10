"""Добавил ограничений полей в сервисы: цена и вложения больше, чем 0

Revision ID: 2ed69396d73d
Revises: 40424c40d282
Create Date: 2025-01-10 16:35:14.363974

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '2ed69396d73d'
down_revision: Union[str, None] = '40424c40d282'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    with op.batch_alter_table('service', schema=None) as batch_op:
        batch_op.create_check_constraint(
            'investment_great_than_zero',
            'investments > 0'
        )
        batch_op.create_check_constraint(
            'price_great_than_zero',
            'price > 0'
        )


def downgrade() -> None:
    with op.batch_alter_table('service', schema=None) as batch_op:
        batch_op.drop_constraint('investment_great_than_zero', type_='check')
        batch_op.drop_constraint('price_great_than_zero', type_='check')
