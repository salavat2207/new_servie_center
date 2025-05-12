"""add test master

Revision ID: 06e2034d7c99
Revises: a340a0d911bd
Create Date: 2025-05-11 19:31:10.837567

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '06e2034d7c99'
down_revision: Union[str, None] = 'a340a0d911bd'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    pass


def downgrade() -> None:
    """Downgrade schema."""
    pass
