import sys
import os

# Chemin absolu vers le répertoire du projet sur PythonAnywhere
project_home = '/var/www/squae_pythonanywhere_com'
if project_home not in sys.path:
    sys.path.insert(0, project_home)

# Ajouter le répertoire parent au PYTHONPATH
parent_dir = os.path.dirname(project_home)
if parent_dir not in sys.path:
    sys.path.insert(0, parent_dir)

# import flask app but need to call it "application" for WSGI to work
from app import create_app

application = create_app()

# Si vous utilisez des variables d'environnement, assurez-vous qu'elles sont chargées
from dotenv import load_dotenv
load_dotenv(os.path.join(project_home, '.env')) 