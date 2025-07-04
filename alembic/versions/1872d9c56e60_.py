"""empty message

Revision ID: 1872d9c56e60
Revises: c4b36712ec40
Create Date: 2025-01-27 20:49:46.257733

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '1872d9c56e60'
down_revision: Union[str, None] = 'c4b36712ec40'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column('social_links', 'social_username',
               existing_type=sa.VARCHAR(length=512),
               nullable=False)
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column('social_links', 'social_username',
               existing_type=sa.VARCHAR(length=512),
               nullable=True)
    # ### end Alembic commands ###
