"""empty message

Revision ID: 0929fde640b3
Revises: 23c5fcfd41f1
Create Date: 2024-12-02 13:00:43.098508
"""

from typing import Sequence, Union

import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

from alembic import op

# revision identifiers, used by Alembic.
revision: str = '0929fde640b3'
down_revision: Union[str, None] = '23c5fcfd41f1'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
	# ### commands auto generated by Alembic - please adjust! ###
	with op.batch_alter_table('transaction', schema=None) as batch_op:
		batch_op.alter_column(
			'transaction_type',
			existing_type=postgresql.ENUM(
				'SALE', 'PURCHASE', name='transactiontype'
			),
			type_=sa.String(),
			existing_nullable=False,
		)

	# ### end Alembic commands ###


def downgrade() -> None:
	# ### commands auto generated by Alembic - please adjust! ###
	with op.batch_alter_table('transaction', schema=None) as batch_op:
		batch_op.alter_column(
			'transaction_type',
			existing_type=sa.String(),
			type_=postgresql.ENUM('SALE', 'PURCHASE', name='transactiontype'),
			existing_nullable=False,
		)

	# ### end Alembic commands ###
