from app import create_app, db
from app.models.category import Category

def create_default_categories():
    app = create_app()
    with app.app_context():
        # Liste des catégories par défaut
        default_categories = [
            "Prêt-à-porter",
            "Accessoires",
            "Chaussures",
            "Maroquinerie",
            "Bijouterie",
            "Lingerie",
            "Sportswear",
            "Vintage",
            "Luxe",
            "Enfant"
        ]
        
        # Vérifier et ajouter les catégories
        for category_name in default_categories:
            # Vérifier si la catégorie existe déjà
            existing_category = Category.query.filter_by(name=category_name).first()
            if not existing_category:
                category = Category(name=category_name)
                db.session.add(category)
                print(f"Catégorie ajoutée : {category_name}")
            else:
                print(f"Catégorie déjà existante : {category_name}")
        
        try:
            db.session.commit()
            print("Catégories créées avec succès !")
        except Exception as e:
            db.session.rollback()
            print(f"Erreur lors de la création des catégories : {str(e)}")

if __name__ == '__main__':
    create_default_categories() 