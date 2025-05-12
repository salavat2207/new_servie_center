"""add test master

Revision ID: a340a0d911bd
Revises: a66e8498b807
Create Date: 2025-05-11 19:31:05.265302

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'a340a0d911bd'
down_revision: Union[str, None] = 'a66e8498b807'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    pass


def downgrade() -> None:
    """Downgrade schema."""
    pass
