"""add routes table

Revision ID: d9e6f2a0f7fe
Revises: 38d69739e913
Create Date: 2026-03-26 20:53:49.328203

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from geoalchemy2.types import Geometry


# revision identifiers, used by Alembic.
revision: str = 'd9e6f2a0f7fe'
down_revision: Union[str, Sequence[str], None] = '38d69739e913'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.create_table('routes',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('distance_m', sa.Float(), nullable=False),
    sa.Column('duration_s', sa.Float(), nullable=False),
    sa.Column('geometry', Geometry(geometry_type='LINESTRING', srid=4326, dimension=2, from_text='ST_GeomFromEWKT', name='geometry', nullable=False), nullable=False),
    sa.Column('user_id', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['user_id'], ['users.id'], name=op.f('fk__routes__user_id__users')),
    sa.PrimaryKeyConstraint('id', name=op.f('pk__routes'))
    )
    op.create_index('idx_routes_geometry', 'routes', ['geometry'], unique=False, postgresql_using='gist', if_not_exists=True)


def downgrade() -> None:
    """Downgrade schema."""
    op.drop_index('idx_routes_geometry', table_name='routes', postgresql_using='gist')
    op.drop_table('routes')
