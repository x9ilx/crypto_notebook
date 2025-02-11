"""Добавил, в модель валюты, поля: путь до изображения и текущая цена

Revision ID: 40424c40d282
Revises: 0e22bc0569bc
Create Date: 2025-01-08 18:18:21.184553

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '40424c40d282'
down_revision: Union[str, None] = '0e22bc0569bc'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
	# ### commands auto generated by Alembic - please adjust! ###
	with op.batch_alter_table('currency', schema=None) as batch_op:
		batch_op.add_column(
			sa.Column('image_path', sa.String(), nullable=True)
		)
		batch_op.add_column(
			sa.Column(
				'current_price',
				sa.Float(),
				nullable=True,
				server_default='0.0',
			)
		)

	op.execute(
		'UPDATE currency SET current_price = 0 WHERE current_price IS NULL'
	)

	with op.batch_alter_table('currency', schema=None) as batch_op:
		batch_op.alter_column('current_price', nullable=False)
	# ### end Alembic commands ###


def downgrade() -> None:
	# ### commands auto generated by Alembic - please adjust! ###
	with op.batch_alter_table('currency', schema=None) as batch_op:
		batch_op.drop_column('current_price')
		batch_op.drop_column('image_path')

	# ### end Alembic commands ###
