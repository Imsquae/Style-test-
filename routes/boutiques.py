from flask import Blueprint, render_template, request, jsonify, redirect, url_for, flash, current_app
from flask_login import login_required, current_user
from app.models import Boutique, Review, Category, BoutiqueVisit, UserFavorite
from app.forms import ReviewForm, AdvancedSearchForm, BoutiqueForm
from app.decorators import check_confirmed
from sqlalchemy import or_
from app.extensions import db
from app.models.review import Review  # Ajout de l'import

bp = Blueprint('boutiques', __name__, url_prefix='/boutiques')

@bp.route('/')
def index():
    boutiques = Boutique.query.all()
    return render_template('boutiques/index.html', boutiques=boutiques)

@bp.route('/<int:id>')
def show(id):
    boutique = Boutique.query.get_or_404(id)
    
    # Enregistrer la visite
    visit = BoutiqueVisit(
        boutique_id=boutique.id,
        user_id=current_user.id if not current_user.is_anonymous else None
    )
    db.session.add(visit)
    db.session.commit()
    
    return render_template('boutiques/detail.html', 
                         boutique=boutique,
                         Review=Review)  # Passage du modèle Review au template

@bp.route('/<int:id>/favorite', methods=['POST'])
@login_required
def toggle_favorite(id):
    boutique = Boutique.query.get_or_404(id)
    if boutique in current_user.favorites:
        current_user.favorites.remove(boutique)
        flash('Boutique retirée des favoris.', 'success')
    else:
        current_user.favorites.append(boutique)
        flash('Boutique ajoutée aux favoris.', 'success')
    db.session.commit()
    return redirect(url_for('boutiques.show', id=id))

@bp.route('/<int:id>/review', methods=['POST'])
@login_required
def add_review(id):
    boutique = Boutique.query.get_or_404(id)
    comment = request.form.get('content')
    rating = request.form.get('rating', type=int)
    
    if not comment or not rating or rating < 1 or rating > 5:
        flash('Veuillez fournir un commentaire et une note valide.', 'error')
        return redirect(url_for('boutiques.show', id=id))
    
    review = Review(
        comment=comment,
        rating=rating,
        reviewer=current_user,
        boutique=boutique
    )
    db.session.add(review)
    db.session.commit()
    flash('Avis ajouté avec succès.', 'success')
    return redirect(url_for('boutiques.show', id=id))

@bp.route('/search', methods=['GET', 'POST'])
def advanced_search():
    form = AdvancedSearchForm()
    
    # Remplir dynamiquement les catégories
    form.category.choices = [('', 'Toutes')] + [
        (str(c.id), c.name) for c in Category.query.all()
    ]
    
    if form.validate_on_submit():
        query = Boutique.query
        
        if form.target_audience.data:
            query = query.filter(Boutique.target_audience == form.target_audience.data)
            
        if form.price_range.data:
            query = query.filter(Boutique.price_range == form.price_range.data)
            
        if form.category.data:
            query = query.filter(Boutique.category_id == form.category.data)
            
        if form.location.data:
            query = query.filter(Boutique.address.ilike(f'%{form.location.data}%'))
            
        boutiques = query.all()
        
        if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
            return jsonify([{
                'id': b.id,
                'name': b.name,
                'description': b.description,
                'address': b.address,
                'rating': db.session.query(db.func.avg(Review.rating))
                    .filter(Review.boutique_id == b.id)
                    .scalar() or 0,
                'category': b.category.name if b.category else None,
                'image_url': url_for('static', 
                                   filename=f'uploads/{b.image_filename}' if b.image_filename 
                                   else 'images/default_boutique.jpg')
            } for b in boutiques])
            
        return render_template('boutiques/search_results.html', 
                             boutiques=boutiques, 
                             form=form)
                             
    return render_template('boutiques/search.html', form=form)

@bp.route('/my-boutiques')
@login_required
def my_boutiques():
    boutiques = current_user.owned_boutiques.all()
    return render_template('boutiques/my_boutiques.html', boutiques=boutiques)

@bp.route('/new', methods=['GET', 'POST'])
@login_required
def new():
    form = BoutiqueForm()
    if form.validate_on_submit():
        boutique = Boutique(
            name=form.name.data,
            description=form.description.data,
            address=form.address.data,
            category_id=form.category_id.data,
            target_audience=form.target_audience.data,
            user_id=current_user.id
        )
        db.session.add(boutique)
        db.session.commit()
        flash('Boutique créée avec succès!', 'success')
        return redirect(url_for('boutiques.show', id=boutique.id))
    return render_template('boutiques/new.html', form=form)

@bp.route('/boutiques/<int:id>/edit', methods=['GET', 'POST'])
@login_required
def edit_boutique(id):
    boutique = Boutique.query.get_or_404(id)
    if boutique.owner.id != current_user.id:
        flash('Vous n\'êtes pas autorisé à modifier cette boutique', 'error')
        return redirect(url_for('boutiques.my_boutiques'))
    # ... reste du code ...     

@bp.route('/boutiques/create', methods=['GET', 'POST'])
@login_required
def create():
    form = BoutiqueForm()
    if form.validate_on_submit():
        boutique = Boutique(
            name=form.name.data,
            description=form.description.data,
            address=form.address.data,
            category_id=form.category.data,
            user_id=current_user.id
        )
        db.session.add(boutique)
        db.session.commit()
        flash('Boutique créée avec succès!', 'success')
        return redirect(url_for('boutiques.show', id=boutique.id))
    return render_template('boutiques/create.html', form=form)

@bp.route('/<int:id>/delete', methods=['POST'])
@login_required
def delete_boutique(id):
    boutique = Boutique.query.get_or_404(id)
    if boutique.user_id != current_user.id and not current_user.is_admin:
        flash('Vous n\'avez pas la permission de supprimer cette boutique', 'error')
        return redirect(url_for('boutiques.my_boutiques'))
    
    try:
        db.session.delete(boutique)
        db.session.commit()
        flash('Boutique supprimée avec succès', 'success')
    except Exception as e:
        db.session.rollback()
        flash('Erreur lors de la suppression de la boutique', 'error')
        current_app.logger.error(f"Erreur suppression boutique: {str(e)}")
    
    return redirect(url_for('boutiques.my_boutiques'))     