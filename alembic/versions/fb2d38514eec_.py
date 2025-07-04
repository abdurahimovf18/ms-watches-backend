"""empty message

Revision ID: fb2d38514eec
Revises: c341dbc01c3d
Create Date: 2025-01-28 17:41:42.756708

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision: str = 'fb2d38514eec'
down_revision: Union[str, None] = 'c341dbc01c3d'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column('brand_images', 'image_type',
               existing_type=postgresql.ENUM('LIGHT_IMAGE', 'DARK_IMAGE', 'PLACEHOLDER', name='brandimagetype'),
               nullable=False)
    op.alter_column('brand_images', 'image_url',
               existing_type=sa.VARCHAR(length=2048),
               nullable=False)
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column('brand_images', 'image_url',
               existing_type=sa.VARCHAR(length=2048),
               nullable=True)
    op.alter_column('brand_images', 'image_type',
               existing_type=postgresql.ENUM('LIGHT_IMAGE', 'DARK_IMAGE', 'PLACEHOLDER', name='brandimagetype'),
               nullable=True)
    # ### end Alembic commands ###
