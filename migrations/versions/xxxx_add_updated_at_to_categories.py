"""Add updated_at column to categories table

Revision ID: xxxx
Revises: previous_revision
Create Date: 2025-05-18 23:46:22.000000

"""
from alembic import op
import sqlalchemy as sa
from datetime import datetime

# revision identifiers, used by Alembic.
revision = 'xxxx'  # remplacer par l'ID généré
down_revision = 'previous_revision'  # remplacer par l'ID de la révision précédente
branch_labels = None
depends_on = None

def upgrade():
    # Ajouter la colonne updated_at
    op.add_column('categories', sa.Column('updated_at', sa.DateTime(), nullable=True))
    
    # Mettre à jour les enregistrements existants
    op.execute("UPDATE categories SET updated_at = created_at WHERE updated_at IS NULL")
    
    # Rendre la colonne non nullable
    op.alter_column('categories', 'updated_at',
                    existing_type=sa.DateTime(),
                    nullable=False,
                    server_default=sa.text('CURRENT_TIMESTAMP'))

def downgrade():
    op.drop_column('categories', 'updated_at') 