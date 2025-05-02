"""add users table

Revision ID: 057cfad0ab73
Revises: 00c64811fd96
Create Date: 2025-05-01 10:32:39.290886

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '057cfad0ab73'
down_revision: Union[str, None] = '00c64811fd96'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table('users', sa.Column('id', sa.Integer(), nullable=False),
                     sa.Column('email', sa.String(), nullable=False), 
                     sa.Column('password', sa.String(), nullable=False),
                     sa.Column('created_at', sa.TIMESTAMP(timezone=True), server_default=sa.text('now()'), nullable=False),
                     sa.PrimaryKeyConstraint('id'), 
                     sa.UniqueConstraint('email')
                    )
    pass


def downgrade() -> None:
    op.drop_table('users')
    pass
