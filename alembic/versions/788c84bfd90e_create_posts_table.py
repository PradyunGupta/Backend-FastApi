"""create posts table

Revision ID: 788c84bfd90e
Revises: 
Create Date: 2025-05-01 10:06:14.395848

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '788c84bfd90e'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table('posts', sa.Column('id', sa.Integer(), nullable=False, primary_key=True), sa.Column('title', sa.String(), nullable=False))
    #sa means sqlalchemy object
    pass


def downgrade() -> None:
    op.drop_table('posts')
    pass
