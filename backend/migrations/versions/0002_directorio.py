import sqlalchemy as sa
from alembic import op

revision = "0002"
down_revision = "0001"
branch_labels = None
depends_on = None


def upgrade():
    op.create_table(
        "institution_directory",
        sa.Column("slug", sa.String(80), primary_key=True),
        sa.Column("name", sa.String(200), nullable=False),
        sa.Column("kind", sa.String(40), nullable=False),
        sa.Column("data", sa.JSON(), nullable=False),
        schema="orienta",
    )
    for name in ("name", "kind"):
        op.create_index(
            f"ix_orienta_institution_directory_{name}",
            "institution_directory",
            [name],
            schema="orienta",
        )


def downgrade():
    op.drop_table("institution_directory", schema="orienta")
