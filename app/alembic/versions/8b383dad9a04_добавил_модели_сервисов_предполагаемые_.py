"""Добавил модели сервисов: Предполагаемые точки покупки и продажи.

Revision ID: 8b383dad9a04
Revises: 3920e885f5b1
Create Date: 2024-12-13 01:26:31.233397
"""

from typing import Sequence, Union

import sqlalchemy as sa

from alembic import op

# revision identifiers, used by Alembic.
revision: str = '8b383dad9a04'
down_revision: Union[str, None] = '3920e885f5b1'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
	# ### commands auto generated by Alembic - please adjust! ###
	op.create_table(
		'service',
		sa.Column('investments', sa.Float(), nullable=False),
		sa.Column('price', sa.Float(), nullable=False),
		sa.Column('service_type', sa.String(), nullable=False),
		sa.Column('currency_id', sa.Integer(), nullable=False),
		sa.Column('id', sa.Integer(), nullable=False),
		sa.Column('user_id', sa.Integer(), nullable=False),
		sa.ForeignKeyConstraint(
			['currency_id'],
			['currency.id'],
		),
		sa.ForeignKeyConstraint(
			['user_id'],
			['user.id'],
		),
		sa.PrimaryKeyConstraint('id'),
	)
	with op.batch_alter_table('service', schema=None) as batch_op:
		batch_op.create_index(
			batch_op.f('ix_service_id'), ['id'], unique=False
		)

	# ### end Alembic commands ###


def downgrade() -> None:
	# ### commands auto generated by Alembic - please adjust! ###
	with op.batch_alter_table('service', schema=None) as batch_op:
		batch_op.drop_index(batch_op.f('ix_service_id'))

	op.drop_table('service')
	# ### end Alembic commands ###
