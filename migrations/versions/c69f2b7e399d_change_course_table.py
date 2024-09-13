"""change  course table

Revision ID: c69f2b7e399d
Revises: ce2d8fe24206
Create Date: 2024-09-13 22:33:19.828629

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'c69f2b7e399d'
down_revision: Union[str, None] = 'ce2d8fe24206'
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