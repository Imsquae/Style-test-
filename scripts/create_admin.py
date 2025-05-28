from app import create_app, db
from app.models import User


def create_admin():
    app = create_app()
    with app.app_context():
        # Vérifie si l'admin existe déjà
        admin = User.query.filter_by(email='eagle@stylehub.ci').first()
        if not admin:
            admin = User(
                username='eagle',
                email='eagle@stylehub.com',
                is_admin=True
            )
            admin.set_password('22457788!')  # Définissez un mot de passe plus sécurisé
            db.session.add(admin)
            db.session.commit()
            print("Compte admin créé avec succès!")
        else:
            print("Un compte admin existe déjà")


if __name__ == '__main__':
    create_admin()