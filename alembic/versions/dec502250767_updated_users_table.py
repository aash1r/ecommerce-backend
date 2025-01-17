"""updated users table

Revision ID: dec502250767
Revises: eb9730d90821
Create Date: 2024-12-20 02:17:50.407502

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision: str = 'dec502250767'
down_revision: Union[str, None] = 'eb9730d90821'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('users', sa.Column('created_At', sa.TIMESTAMP(timezone=True), server_default=sa.text('now()'), nullable=False))
    op.drop_constraint('users_email_key', 'users', type_='unique')
    op.drop_column('users', 'created_at')
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('users', sa.Column('created_at', postgresql.TIMESTAMP(), server_default=sa.text('now()'), autoincrement=False, nullable=False))
    op.create_unique_constraint('users_email_key', 'users', ['email'])
    op.drop_column('users', 'created_At')
    # ### end Alembic commands ###
