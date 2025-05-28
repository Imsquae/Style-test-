from app import create_app, db
from app.models import User, Category, Boutique

def reset_database():
    app = create_app()
    with app.app_context():
        # Supprimer toutes les tables
        db.drop_all()
        # Recréer toutes les tables
        db.create_all()
        
        # Recréer l'administrateur
        admin = User(
            username='Eagle',
            email='eagle@stylehub.com',
            is_admin=True
        )
        admin.set_password('22457788!')
        db.session.add(admin)
        
        # Créer quelques catégories
        categories = [
            Category(name='Vêtements'),
            Category(name='Chaussures'),
            Category(name='Accessoires'),
            Category(name='Bijoux')
        ]
        db.session.add_all(categories)
        
        # Créer quelques boutiques
        boutiques = [
            Boutique(
                name='Fashion Store',
                address='123 Rue de la Mode',
                description='Boutique de mode tendance',
                category=categories[0]
            ),
            Boutique(
                name='Shoe Paradise',
                address='456 Avenue du Style',
                description='Les meilleures chaussures en ville',
                category=categories[1]
            )
        ]
        db.session.add_all(boutiques)
        
        db.session.commit()
        print("Base de données réinitialisée avec succès!")

if __name__ == '__main__':
    reset_database() 