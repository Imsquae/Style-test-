"""update warning count default value

Revision ID: xxx
Revises: previous_revision
Create Date: 2025-05-18 23:30:00.000000

"""
from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision = 'xxx'  # remplacer par l'ID généré
down_revision = 'previous_revision'  # remplacer par la révision précédente
branch_labels = None
depends_on = None

def upgrade():
    # Mettre à jour tous les utilisateurs existants pour définir warning_count à 0 s'il est NULL
    op.execute("UPDATE users SET warning_count = 0 WHERE warning_count IS NULL")

def downgrade():
    # Pas de downgrade nécessaire car nous ne voulons pas revenir à NULL
    pass 