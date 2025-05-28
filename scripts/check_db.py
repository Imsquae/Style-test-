from app import create_app, db
from app.models.category import Category
from app.models.boutique import Boutique

def check_database():
    app = create_app()
    with app.app_context():
        print("=== Vérification de la base de données ===")
        
        # Vérifier les catégories
        categories = Category.query.all()
        print(f"\nNombre de catégories : {len(categories)}")
        for category in categories:
            print(f"- {category.name} (ID: {category.id})")
        
        # Vérifier les boutiques
        boutiques = Boutique.query.all()
        print(f"\nNombre de boutiques : {len(boutiques)}")
        for boutique in boutiques:
            print(f"- {boutique.name} (ID: {boutique.id}, Catégorie: {boutique.category_id})")

if __name__ == '__main__':
    check_database() 