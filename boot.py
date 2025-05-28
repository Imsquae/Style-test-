from app import create_app, db
from app.models.user import User

def init_db():
    app = create_app()
    with app.app_context():
        # Créer les tables
        db.create_all()
        
        # Créer un admin si aucun n'existe
        if not User.query.filter_by(email='eagle@stylehub.com').first():
            admin = User(
                username='Eagle',
                email='eagle@stylehub.com',
                is_admin=True
            )
            admin.set_password('22457788!')
            db.session.add(admin)
            db.session.commit()
            print('Admin créé avec succès!')
        else:
            print('Admin existe déjà!')

if __name__ == '__main__':
    init_db() 