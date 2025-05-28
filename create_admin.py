from app import create_app, db
from app.models.user import User
import sys

def create_admin():
    app = create_app()
    with app.app_context():
        # Vérifie si l'admin existe déjà
        admin = User.query.filter_by(email='admin@stylehub.com').first()
        if admin is None:
            try:
                admin = User(
                    username='Admin',
                    email='admin@stylehub.com',
                    first_name='Administrateur',
                    last_name='StyleHub',
                    is_admin = True,
                    is_confirmed=True,  # L'admin est automatiquement confirmé
                    bio='Administrateur principal de StyleHub',
                    location='Paris, France'
                )
                # Définir un mot de passe plus sécurisé
                password = 'Admin@StyleHub2024'  # À changer après la première connexion!
                admin.set_password(password)
                
                db.session.add(admin)
                db.session.commit()
                
                print('\n=== Création de l\'administrateur réussie ===')
                print(f'Email: {admin.email}')
                print(f'Mot de passe: {password}')
                print('\nIMPORTANT: Veuillez changer ce mot de passe après votre première connexion!')
                print('=============================================\n')
                
            except Exception as e:
                print('\n=== Erreur lors de la création de l\'administrateur ===')
                print(f'Erreur: {str(e)}')
                print('=====================================================\n')
                db.session.rollback()
                sys.exit(1)
        else:
            print('\n=== Information ===')
            print('Un administrateur existe déjà avec l\'email:', admin.email)
            print('===================\n')
            sys.exit(0)

if __name__ == '__main__':
    print('\nDémarrage de la création de l\'administrateur...')
    create_admin() 