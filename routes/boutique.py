from flask import Blueprint, render_template, flash, request, redirect, url_for, current_app
from flask_login import login_required, current_user
from app.models.category import Category
from app.models.boutique import Boutique
from app.extensions import db
import os
from werkzeug.utils import secure_filename
from datetime import datetime

# Définition du blueprint
bp = Blueprint('boutique', __name__, url_prefix='/boutiques')

@bp.route('/new', methods=['GET', 'POST'])
@login_required
def create():
    current_app.logger.info("Accès à la route de création de boutique")
    
    # Vérifier et créer le dossier d'upload si nécessaire
    upload_folder = current_app.config['UPLOAD_FOLDER']
    if not os.path.exists(upload_folder):
        os.makedirs(upload_folder)
        current_app.logger.info(f"Création du dossier d'upload: {upload_folder}")

    # Récupérer les catégories et vérifier qu'il y en a
    try:
        categories = Category.query.order_by(Category.name).all()
        current_app.logger.info(f"Nombre de catégories trouvées : {len(categories)}")
        
        if not categories:
            current_app.logger.warning("Aucune catégorie trouvée dans la base de données")
            # Exécuter le script de création des catégories par défaut
            from scripts.create_categories import create_default_categories
            create_default_categories()
            categories = Category.query.order_by(Category.name).all()
            current_app.logger.info(f"Catégories créées, nouveau nombre : {len(categories)}")
    except Exception as e:
        current_app.logger.error(f"Erreur lors de la récupération des catégories : {str(e)}")
        flash('Erreur lors du chargement des catégories', 'error')
        return redirect(url_for('boutique.my_boutiques'))

    if request.method == 'POST':
        current_app.logger.info("Traitement d'une soumission de formulaire")
        try:
            # Récupération des données du formulaire
            form_data = {
                'name': request.form.get('name', '').strip(),
                'category_id': request.form.get('category_id'),
                'description': request.form.get('description', '').strip(),
                'address': request.form.get('address', '').strip(),
                'target_audience': request.form.get('target_audience')
            }
            
            current_app.logger.info(f"Données du formulaire reçues : {form_data}")
            
            # Validation des données
            for field, value in form_data.items():
                if not value:
                    flash(f'Le champ {field} est requis', 'error')
                    current_app.logger.warning(f"Champ manquant : {field}")
                    return redirect(url_for('boutique.create'))
            
            # Vérification de la catégorie
            category = Category.query.get(form_data['category_id'])
            if not category:
                flash('Catégorie invalide', 'error')
                current_app.logger.warning(f"Catégorie invalide : {form_data['category_id']}")
                return redirect(url_for('boutique.create'))
            
            # Traitement de l'image
            image_filename = None
            if 'image' in request.files:
                image = request.files['image']
                if image and image.filename:
                    current_app.logger.info(f"Traitement de l'image : {image.filename}")
                    # Vérification de l'extension
                    allowed_extensions = {'png', 'jpg', 'jpeg', 'gif'}
                    if '.' not in image.filename or \
                       image.filename.rsplit('.', 1)[1].lower() not in allowed_extensions:
                        flash('Format d\'image non autorisé', 'error')
                        return redirect(url_for('boutique.create'))
                    
                    filename = secure_filename(image.filename)
                    image_filename = f"{datetime.utcnow().strftime('%Y%m%d_%H%M%S')}_{filename}"
                    image_path = os.path.join(upload_folder, image_filename)
                    
                    try:
                        image.save(image_path)
                        current_app.logger.info(f"Image sauvegardée: {image_path}")
                    except Exception as e:
                        current_app.logger.error(f"Erreur sauvegarde image: {str(e)}")
                        flash('Erreur lors de la sauvegarde de l\'image', 'error')
                        return redirect(url_for('boutique.create'))
            
            # Création de la boutique
            boutique = Boutique(
                name=form_data['name'],
                category_id=form_data['category_id'],
                description=form_data['description'],
                address=form_data['address'],
                target_audience=form_data['target_audience'],
                image_filename=image_filename,
                user_id=current_user.id
            )
            
            db.session.add(boutique)
            db.session.commit()
            
            current_app.logger.info(f"Boutique créée avec succès : {boutique.id}")
            flash('Boutique créée avec succès !', 'success')
            return redirect(url_for('boutique.my_boutiques'))
            
        except Exception as e:
            db.session.rollback()
            current_app.logger.error(f"Erreur création boutique: {str(e)}")
            flash('Une erreur est survenue lors de la création de la boutique', 'error')
            return redirect(url_for('boutique.create'))
    
    # GET request
    return render_template('boutique/create.html', categories=categories) 