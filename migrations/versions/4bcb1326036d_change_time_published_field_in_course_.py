"""change time published field in course table

Revision ID: 4bcb1326036d
Revises: 888d29269f77
Create Date: 2024-09-13 22:22:38.231862

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '4bcb1326036d'
down_revision: Union[str, None] = '888d29269f77'
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