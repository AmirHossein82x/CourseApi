"""change  course table

Revision ID: ce2d8fe24206
Revises: 4bcb1326036d
Create Date: 2024-09-13 22:25:27.889367

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'ce2d8fe24206'
down_revision: Union[str, None] = '4bcb1326036d'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column('promotion', 'discount',
               existing_type=sa.REAL(),
               type_=sa.Float(precision=1, asdecimal=True),
               existing_nullable=False)
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column('promotion', 'discount',
               existing_type=sa.Float(precision=1, asdecimal=True),
               type_=sa.REAL(),
               existing_nullable=False)
    # ### end Alembic commands ###
