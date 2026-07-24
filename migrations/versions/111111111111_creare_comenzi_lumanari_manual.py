"""
Creare manuala tabela comenzi_lumanari.
Migrare securizata de nivel Senior: Protejeaza datele existente din Neon Cloud.
"""

from alembic import op
import sqlalchemy as sa

# Identificatorii de versiune ceruti nativ de motorul Alembic
revision = "111111111111"
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:
    """Cream exclusiv tabela de legatura pentru produse fara a afecta restul inventarului."""
    op.create_table(
        "comenzi_lumanari",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("id_comanda", sa.Integer(), nullable=False),
        sa.Column("id_lumanare", sa.Integer(), nullable=False),
        sa.Column("cantitate", sa.Integer(), nullable=False),
        sa.Column("pret_salvat", sa.Float(), nullable=False),
        sa.ForeignKeyConstraint(
            ["id_comanda"], ["comenzi.id_comanda"], ondelete="CASCADE"
        ),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index("ix_comenzi_lumanari_id", "comenzi_lumanari", ["id"], unique=False)


def downgrade() -> None:
    """Anularea modificarilor in caz de rollback structural."""
    op.drop_index("ix_comenzi_lumanari_id", table_name="comenzi_lumanari")
    op.drop_table("comenzi_lumanari")

