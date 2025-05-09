"""add content column to post table

Revision ID: 00c64811fd96
Revises: 788c84bfd90e
Create Date: 2025-05-01 10:28:21.497648

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '00c64811fd96'
down_revision: Union[str, None] = '788c84bfd90e'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column('posts', sa.Column('content', sa.String(), nullable=False))
    pass


def downgrade() -> None:
    op.drop_column('posts', 'content')
    pass
