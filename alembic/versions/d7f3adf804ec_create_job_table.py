"""create job table

Revision ID: d7f3adf804ec
Revises:
Create Date: 2025-03-18 17:21:11.483182

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = "d7f3adf804ec"
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


# I am wondering if we can use the sqlalchemy orm for this?
def upgrade() -> None:
    """Upgrade schema."""
    # Create the new related table
    op.create_table(
        "job",
        sa.Column("id", sa.Integer, primary_key=True),
        sa.Column("name", sa.String(50), nullable=False),
        sa.Column("permission_level", sa.Integer),
    )

    # Insert a default job
    op.execute("INSERT INTO job (name, permission_level) VALUES ('Unknown Job', 0)")

    # Get the ID of the newly inserted job
    connection = op.get_bind()
    result = connection.execute(
        sa.text("SELECT id FROM job WHERE name = 'Unknown Job'")
    )
    default_id = result.scalar()

    # Add the foreign key constraint to the existing table
    op.add_column(
        "users",
        sa.Column(
            "job_id",
            sa.Integer,
            sa.ForeignKey("job.id"),
            server_default=sa.text(str(default_id)),
        ),
    )


def downgrade() -> None:
    """Downgrade schema."""
    # Remove the foreign key constraint
    op.drop_column("users", "job_id")

    # Drop the related table
    op.drop_table("job")
