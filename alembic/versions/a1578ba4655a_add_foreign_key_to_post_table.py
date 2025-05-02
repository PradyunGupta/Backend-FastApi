"""add foreign key to post table

Revision ID: a1578ba4655a
Revises: 057cfad0ab73
Create Date: 2025-05-02 08:35:45.104892

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'a1578ba4655a'
down_revision: Union[str, None] = '057cfad0ab73'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column('posts', sa.Column('owner_id', sa.Integer(), nullable=False))
    op.create_foreign_key('posts_users_fk', source_table="posts", referent_table="users", 
                          local_cols=["owner_id"], remote_cols=["id"], ondelete="CASCADE")
    pass


def downgrade() -> None:
    op.drop_constraint('posts_users_fk', table_name="posts", type_="foreignkey")
    op.drop_column('posts', 'owner_id')
    pass
