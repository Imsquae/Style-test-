from flask import Blueprint, render_template, redirect, url_for, flash, request, jsonify, abort
from flask_login import login_required, current_user
from app.models import User, Boutique, Review, Category, BoutiqueVisit, UserFavorite, UserEngagement
from app.extensions import db
from functools import wraps
from app.decorators import admin_required
from datetime import datetime, timedelta
import os
from flask import current_app

bp = Blueprint('admin', __name__, url_prefix='/admin')


def admin_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not current_user.is_admin:
            abort(403)  # Accès interdit
        return f(*args, **kwargs)
    decorated_function.__name__ = f.__name__
    return decorated_function


@bp.route('/dashboard')
@login_required
@admin_required
def dashboard():
    users = User.query.all()
    boutiques = Boutique.query.all()
    categories = Category.query.all()
    return render_template('admin/dashboard.html', 
                         users=users, 
                         boutiques=boutiques,
                         categories=categories)


@bp.route('/users')
@login_required
@admin_required
def manage_users():
    users = User.query.all()
    return render_template('admin/users/index.html', users=users)


@bp.route('/users/<int:id>/edit', methods=['GET', 'POST'])
@login_required
@admin_required
def edit_user(id):
    user = User.query.get_or_404(id)
    if request.method == 'POST':
        user.username = request.form['username']
        user.email = request.form['email']
        if request.form.get('is_admin'):
            user.is_admin = True
        db.session.commit()
        flash('Utilisateur mis à jour avec succès.', 'success')
        return redirect(url_for('admin.manage_users'))
    return render_template('admin/users/edit.html', user=user)


@bp.route('/users/<int:id>/delete', methods=['POST'])
@login_required
@admin_required
def delete_user(id):
    user = User.query.get_or_404(id)
    if user.is_admin:
        flash('Impossible de supprimer un administrateur.', 'error')
    else:
        db.session.delete(user)
        db.session.commit()
        flash('Utilisateur supprimé avec succès.', 'success')
    return redirect(url_for('admin.manage_users'))


@bp.route('/users/<int:id>/moderate', methods=['GET', 'POST'])
@login_required
@admin_required
def moderate_user(id):
    user = User.query.get_or_404(id)
    
    if request.method == 'POST':
        action = request.form.get('action')
        reason = request.form.get('reason', '')
        
        if action == 'warn':
            if user.warning_count is None:
                user.warning_count = 0
            user.warning_count += 1
            user.last_warning = datetime.utcnow()
            user.moderation_notes = f"{user.moderation_notes or ''}\n[{datetime.utcnow()}] Avertissement: {reason}"
            flash(f'Avertissement envoyé à {user.username}', 'warning')
            
        elif action == 'ban':
            user.is_banned = True
            user.ban_reason = reason
            user.banned_at = datetime.utcnow()
            user.moderation_notes = f"{user.moderation_notes or ''}\n[{datetime.utcnow()}] Banni: {reason}"
            flash(f'Utilisateur {user.username} banni', 'danger')
            
        elif action == 'unban':
            user.is_banned = False
            user.ban_reason = None
            user.banned_at = None
            user.moderation_notes = f"{user.moderation_notes or ''}\n[{datetime.utcnow()}] Débanni"
            flash(f'Utilisateur {user.username} débanni', 'success')
            
        elif action == 'reset_warnings':
            user.warning_count = 0
            user.last_warning = None
            user.moderation_notes = f"{user.moderation_notes or ''}\n[{datetime.utcnow()}] Avertissements réinitialisés"
            flash(f'Avertissements réinitialisés pour {user.username}', 'info')
        
        db.session.commit()
        return redirect(url_for('admin.manage_users'))
        
    return render_template('admin/users/moderate.html', user=user)


@bp.route('/users/<int:id>/moderation-history')
@login_required
@admin_required
def user_moderation_history(id):
    user = User.query.get_or_404(id)
    return render_template('admin/users/moderation_history.html', user=user)


@bp.route('/boutiques')
@login_required
@admin_required
def manage_boutiques():
    boutiques = Boutique.query.all()
    return render_template('admin/boutiques/index.html', boutiques=boutiques)


@bp.route('/boutiques/new', methods=['GET', 'POST'])
@login_required
@admin_required
def new_boutique():
    if request.method == 'POST':
        try:
            # Récupérer les données du formulaire
            name = request.form.get('name')
            description = request.form.get('description')
            category_id = request.form.get('category_id')
            address = request.form.get('address')
            
            # Validation des données
            if not all([name, description, category_id]):
                flash('Tous les champs obligatoires doivent être remplis.', 'danger')
                return redirect(url_for('admin.new_boutique'))
            
            # Vérifier si la catégorie existe
            category = Category.query.get(category_id)
            if not category:
                flash('Catégorie invalide.', 'danger')
                return redirect(url_for('admin.new_boutique'))
            
            # Créer la nouvelle boutique
            boutique = Boutique(
                name=name,
                description=description,
                category_id=category_id,
                address=address,
                user_id=current_user.id
            )
            
            db.session.add(boutique)
            db.session.commit()
            
            flash('Boutique créée avec succès.', 'success')
            return redirect(url_for('admin.manage_boutiques'))
            
        except Exception as e:
            db.session.rollback()
            flash(f'Erreur lors de la création de la boutique: {str(e)}', 'danger')
            return redirect(url_for('admin.new_boutique'))
    
    # GET request - afficher le formulaire
    categories = Category.query.order_by(Category.name).all()
    return render_template('admin/boutiques/new.html', categories=categories)


@bp.route('/boutiques/<int:id>/edit', methods=['GET', 'POST'])
@login_required
@admin_required
def edit_boutique(id):
    boutique = Boutique.query.get_or_404(id)
    if request.method == 'POST':
        boutique.name = request.form['name']
        boutique.address = request.form['address']
        boutique.description = request.form['description']
        boutique.category_id = request.form['category_id']
        db.session.commit()
        flash('Boutique mise à jour avec succès.', 'success')
        return redirect(url_for('admin.manage_boutiques'))
    categories = Category.query.all()
    return render_template('admin/boutiques/edit.html', boutique=boutique, categories=categories)


@bp.route('/boutiques/<int:id>/delete', methods=['POST'])
@login_required
@admin_required
def delete_boutique(id):
    boutique = Boutique.query.get_or_404(id)
    try:
        # Delete related visits first
        BoutiqueVisit.query.filter_by(boutique_id=boutique.id).delete()
        db.session.delete(boutique)
        db.session.commit()
        flash('Boutique supprimée avec succès', 'success')
    except Exception as e:
        db.session.rollback()
        flash('Erreur lors de la suppression de la boutique', 'error')
        current_app.logger.error(f"Erreur suppression boutique: {str(e)}")
    
    return redirect(url_for('admin.manage_boutiques'))


@bp.route('/categories', methods=['GET', 'POST'])
@login_required
@admin_required
def manage_categories():
    if request.method == 'POST':
        name = request.form.get('name', '').strip()
        if name:
            try:
                category = Category(name=name)
                db.session.add(category)
                db.session.commit()
                flash('Catégorie ajoutée avec succès', 'success')
            except Exception as e:
                db.session.rollback()
                flash('Erreur lors de l\'ajout de la catégorie', 'error')
    
    categories = Category.query.order_by(Category.name).all()
    return render_template('admin/categories/index.html', categories=categories)


@bp.route('/categories/new', methods=['GET', 'POST'])
@login_required
@admin_required
def new_category():
    if request.method == 'POST':
        name = request.form.get('name')
        if name:
            category = Category(name=name)
            db.session.add(category)
            db.session.commit()
            flash('Catégorie créée avec succès.', 'success')
            return redirect(url_for('admin.manage_categories'))
    return render_template('admin/categories/form.html', category=None)


@bp.route('/categories/<int:id>/edit', methods=['GET', 'POST'])
@login_required
@admin_required
def edit_category(id):
    category = Category.query.get_or_404(id)
    if request.method == 'POST':
        name = request.form.get('name')
        if name:
            category.name = name
            db.session.commit()
            flash('Catégorie mise à jour avec succès.', 'success')
            return redirect(url_for('admin.manage_categories'))
    return render_template('admin/categories/form.html', category=category)


@bp.route('/categories/<int:id>/delete', methods=['POST'])
@login_required
@admin_required
def delete_category(id):
    category = Category.query.get_or_404(id)
    db.session.delete(category)
    db.session.commit()
    flash('Catégorie supprimée avec succès.', 'success')
    return redirect(url_for('admin.manage_categories'))


@bp.route('/stats')
@login_required
@admin_required
def stats():
    # Calcul des statistiques pour les 7 derniers jours
    end_date = datetime.now()
    start_date = end_date - timedelta(days=7)
    
    # Préparation des données pour le graphique
    dates = []
    new_users = []
    new_boutiques = []
    
    for i in range(7):
        date = end_date - timedelta(days=i)
        next_date = date + timedelta(days=1)
        
        dates.insert(0, date.strftime('%Y-%m-%d'))
        
        users_count = User.query.filter(
            User.created_at >= date,
            User.created_at < next_date
        ).count()
        new_users.insert(0, users_count)
        
        boutiques_count = Boutique.query.filter(
            Boutique.created_at >= date,
            Boutique.created_at < next_date
        ).count()
        new_boutiques.insert(0, boutiques_count)
    
    return render_template('admin/stats.html',
                         dates=dates,
                         new_users=new_users,
                         new_boutiques=new_boutiques)


@bp.route('/logs')
@login_required
@admin_required
def view_logs():
    log_path = os.path.join(current_app.root_path, '..', 'logs', 'stylehub.log')
    logs = []
    
    if os.path.exists(log_path):
        with open(log_path, 'r') as f:
            # Lire les 100 dernières lignes
            logs = f.readlines()[-100:]
    
    return render_template('admin/logs.html', logs=logs)


@bp.route('/detailed-stats')
@login_required
@admin_required
def detailed_stats():
    # Statistiques des boutiques
    boutique_stats = db.session.query(
        Boutique.name,
        db.func.count(BoutiqueVisit.id).label('visit_count'),
        db.func.count(Review.id).label('review_count'),
        db.func.count(UserFavorite.id).label('favorite_count')
    ).outerjoin(BoutiqueVisit).outerjoin(Review).outerjoin(UserFavorite)\
     .group_by(Boutique.id)\
     .order_by(db.desc('visit_count'))\
     .all()
    
    # Statistiques d'engagement utilisateur
    user_stats = db.session.query(
        User.username,
        db.func.count(Review.id).label('reviews'),
        db.func.count(UserFavorite.id).label('favorites')
    ).outerjoin(Review).outerjoin(UserFavorite)\
     .group_by(User.id)\
     .order_by(db.desc('reviews'))\
     .limit(10)\
     .all()
    
    # Statistiques temporelles
    today = datetime.utcnow().date()
    visits_by_day = db.session.query(
        db.func.date(BoutiqueVisit.timestamp).label('date'),
        db.func.count(BoutiqueVisit.id).label('visits')
    ).group_by('date')\
     .order_by(db.desc('date'))\
     .limit(30)\
     .all()
    
    return render_template('admin/detailed_stats.html',
                         boutique_stats=boutique_stats,
                         user_stats=user_stats,
                         visits_by_day=visits_by_day)


@bp.route('/admin')
@login_required
@admin_required
def admin_panel():
    # Statistiques générales
    total_users = User.query.count()
    total_boutiques = Boutique.query.count()
    total_reviews = Review.query.count()
    
    # Derniers utilisateurs inscrits
    recent_users = User.query.order_by(User.created_at.desc()).limit(5).all()
    
    # Dernières boutiques créées
    recent_boutiques = Boutique.query.order_by(Boutique.created_at.desc()).limit(5).all()
    
    return render_template('admin/panel.html',
                         total_users=total_users,
                         total_boutiques=total_boutiques,
                         total_reviews=total_reviews,
                         recent_users=recent_users,
                         recent_boutiques=recent_boutiques)


@bp.route('/banned-users')
@login_required
def banned_users():
    if not current_user.is_admin:
        flash('Accès non autorisé', 'error')
        return redirect(url_for('main.index'))
    
    banned_users = User.query.filter_by(is_banned=True).all()
    return render_template('admin/banned_users.html', users=banned_users)


@bp.route('/users/<int:user_id>/unban', methods=['POST'])
@login_required
def unban_user(user_id):
    if not current_user.is_admin:
        flash('Accès non autorisé', 'error')
        return redirect(url_for('main.index'))
    
    user = User.query.get_or_404(user_id)
    if user.is_banned:
        user.is_banned = False
        user.ban_reason = None
        user.banned_at = None
        db.session.commit()
        flash(f'Utilisateur {user.username} a été débanni avec succès', 'success')
    else:
        flash('Cet utilisateur n\'est pas banni', 'warning')
    
    return redirect(url_for('admin.banned_users')) 