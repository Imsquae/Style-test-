from app import create_app
from app.extensions import db, socketio
from app.models.user import User
from app.models.boutique import Boutique
from app.models.category import Category
from app.models.notification import Notification
from app.models.stats import BoutiqueStats, UserActivity
from app.models.location import Location

app = create_app()

with app.app_context():
    # Import models

    # Create tables
    db.create_all()

if __name__ == '__main__':
    app.run(debug=True)





