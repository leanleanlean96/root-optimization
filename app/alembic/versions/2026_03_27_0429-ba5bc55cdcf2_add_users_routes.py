"""add users & routes

Revision ID: ba5bc55cdcf2
Revises:
Create Date: 2026-03-27 04:29:28.434370

"""

import geoalchemy2
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision: str = "ba5bc55cdcf2"
down_revision: Union[str, Sequence[str], None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.create_table(
        "users",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("name", sa.String(length=30), nullable=False),
        sa.Column("email", sa.String(length=225), nullable=False),
        sa.Column("is_active", sa.Boolean(), nullable=False, server_default=sa.true()),
        sa.PrimaryKeyConstraint("id", name=op.f("pk__users")),
        sa.UniqueConstraint("email", name=op.f("uq__users__email")),
    )
    op.create_table(
        "routes",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("distance_m", sa.Float(), nullable=False),
        sa.Column("duration_s", sa.Float(), nullable=False),
        sa.Column(
            "geometry",
            geoalchemy2.types.Geometry(
                geometry_type="LINESTRING",
                srid=4326,
                dimension=2,
                from_text="ST_GeomFromEWKT",
                name="geometry",
                nullable=False,
            ),
            nullable=False,
        ),
        sa.Column(
            "is_deleted", sa.Boolean(), nullable=False, server_default=sa.false()
        ),
        sa.Column("user_id", sa.Integer(), nullable=False),
        sa.ForeignKeyConstraint(
            ["user_id"], ["users.id"], name=op.f("fk__routes__user_id__users")
        ),
        sa.PrimaryKeyConstraint("id", name=op.f("pk__routes")),
    )


def downgrade() -> None:
    """Downgrade schema."""
    op.drop_table("routes")
    op.drop_table("users")
    # ### end Alembic commands ###
