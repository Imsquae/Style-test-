from app import create_app, db
from app.models.user import User
import sys

def delete_admins():
    app = create_app()
    with app.app_context():
        try:
            # Récupérer tous les administrateurs
            admins = User.query.filter_by(is_admin=True).all()
            
            if not admins:
                print('\n=== Information ===')
                print('Aucun administrateur trouvé dans la base de données.')
                print('===================\n')
                sys.exit(0)
            
            # Afficher les administrateurs trouvés
            print('\n=== Administrateurs trouvés ===')
            for admin in admins:
                print(f'- {admin.username} ({admin.email})')
            print('==============================\n')
            
            # Demander confirmation
            confirmation = input('Êtes-vous sûr de vouloir supprimer tous les administrateurs? (oui/non): ').lower()
            
            if confirmation != 'oui':
                print('\n=== Opération annulée ===')
                print('Suppression des administrateurs annulée par l\'utilisateur.')
                print('========================\n')
                sys.exit(0)
            
            # Supprimer les administrateurs
            for admin in admins:
                db.session.delete(admin)
            
            db.session.commit()
            
            print('\n=== Suppression réussie ===')
            print(f'{len(admins)} administrateur(s) ont été supprimé(s) avec succès.')
            print('==========================\n')
            
        except Exception as e:
            print('\n=== Erreur lors de la suppression des administrateurs ===')
            print(f'Erreur: {str(e)}')
            print('========================================================\n')
            db.session.rollback()
            sys.exit(1)

if __name__ == '__main__':
    print('\nDémarrage de la suppression des administrateurs...')
    delete_admins() 