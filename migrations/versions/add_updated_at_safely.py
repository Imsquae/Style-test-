"""Add updated_at column safely

Revision ID: xxxx
Revises: previous_revision
Create Date: 2025-05-18 23:48:03.000000

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
    # Vérifier si la colonne existe déjà
    conn = op.get_bind()
    inspector = sa.inspect(conn)
    columns = [col['name'] for col in inspector.get_columns('categories')]
    
    if 'updated_at' not in columns:
        # Ajouter la colonne avec une valeur par défaut
        op.add_column('categories', 
                     sa.Column('updated_at', 
                             sa.DateTime(), 
                             nullable=True,
                             server_default=sa.text('CURRENT_TIMESTAMP')))
        
        # Mettre à jour les enregistrements existants
        op.execute("UPDATE categories SET updated_at = created_at WHERE updated_at IS NULL")
        
        # Rendre la colonne non nullable
        op.alter_column('categories', 'updated_at',
                       existing_type=sa.DateTime(),
                       nullable=False)

def downgrade():
    op.drop_column('categories', 'updated_at') 