"""drop is_active from routes table

Revision ID: 457a7d0e4443
Revises: c053c58c1a34
Create Date: 2026-05-06 02:38:36.944258

"""
from typing import Sequence, Union

import sqlalchemy as sa
from alembic import op

# revision identifiers, used by Alembic.
revision: str = '457a7d0e4443'
down_revision: Union[str, Sequence[str], None] = 'c053c58c1a34'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    # Drop is_active column from routes table
    op.drop_column('routes', 'is_active')


def downgrade() -> None:
    """Downgrade schema."""
    # Add is_active column back to routes table
    op.add_column('routes', sa.Column('is_active', sa.Boolean(), default=True, nullable=False))
