"""create job table

Revision ID: d7f3adf804ec
Revises: 
Create Date: 2025-03-18 17:21:11.483182

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'd7f3adf804ec'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    # Create the new related table
    op.create_table(
        'job',
        sa.Column('id', sa.Integer, primary_key=True),
        sa.Column('name', sa.String(50), nullable=False),
        sa.Column('description', sa.Text),
    )

    # Add the foreign key constraint to the existing table
    op.add_column('users', sa.Column('job_id', sa.Integer, sa.ForeignKey('job.id')))


def downgrade() -> None:
    """Downgrade schema."""
    # Remove the foreign key constraint
    op.drop_column('users', 'job_id')

    # Drop the related table
    op.drop_table('job')
