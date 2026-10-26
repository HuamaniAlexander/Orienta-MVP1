import sqlalchemy as sa
from alembic import op

revision = "0003"
down_revision = "0002"
branch_labels = None
depends_on = None


def upgrade():
    op.create_table(
        "institutional_program",
        sa.Column("id", sa.String(100), primary_key=True),
        sa.Column(
            "institution_slug",
            sa.String(80),
            sa.ForeignKey("orienta.institution_directory.slug"),
            nullable=False,
        ),
        sa.Column(
            "career_code", sa.Integer(), sa.ForeignKey("orienta.career.code"), nullable=False
        ),
        sa.Column("data", sa.JSON(), nullable=False),
        schema="orienta",
    )
    for column in ("institution_slug", "career_code"):
        op.create_index(
            "ix_orienta_institutional_program_" + column,
            "institutional_program",
            [column],
            schema="orienta",
        )


def downgrade():
    op.drop_table("institutional_program", schema="orienta")
