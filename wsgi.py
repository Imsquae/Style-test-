import os
import sys

# Ajouter le répertoire du projet au PYTHONPATH
project_home = os.path.dirname(os.path.abspath(__file__))
if project_home not in sys.path:
    sys.path.insert(0, project_home)

# Importer l'application Flask
from app import create_app

# Créer l'application
application = create_app()

# Si vous utilisez des variables d'environnement, assurez-vous qu'elles sont chargées
from dotenv import load_dotenv
load_dotenv(os.path.join(project_home, '.env'))

if __name__ == '__main__':
    application.run() 
