"""empty message

Revision ID: b0d9c52e4766
Revises: 843831a0eac8
Create Date: 2025-02-15 15:34:42.485686

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'b0d9c52e4766'
down_revision: Union[str, None] = '843831a0eac8'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('channel_members', sa.Column('is_connected', sa.Boolean(), nullable=False))
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('channel_members', 'is_connected')
    # ### end Alembic commands ###
