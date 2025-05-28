from flask import Blueprint, render_template, redirect, url_for, flash, request, current_app
from flask_login import login_required, current_user
from werkzeug.utils import secure_filename
import os
from app.forms import ProfileForm, ChangePasswordForm, PostForm, EditProfileForm
from app.models.user import User
from app.models.post import Post, Comment, Like
from app.models.boutique import Boutique
from app.models.review import Review
from app.extensions import db

bp = Blueprint('profile', __name__)

@bp.route('/profile')
@login_required
def profile_view():
    # Récupérer les informations de l'utilisateur
    user = User.query.get_or_404(current_user.id)
    
    # Récupérer les boutiques de l'utilisateur
    owned_boutiques = user.owned_boutiques.all()
    
    # Récupérer les avis de l'utilisateur
    user_reviews = user.reviews.all()
    
    # Récupérer les boutiques favorites (sans .all() car c'est déjà une liste)
    favorite_boutiques = user.favorites
    
    return render_template('profile/profile.html',
                         user=user,
                         owned_boutiques=owned_boutiques,
                         user_reviews=user_reviews,
                         favorite_boutiques=favorite_boutiques)

@bp.route('/profile/edit', methods=['GET', 'POST'])
@login_required
def edit_profile():
    form = EditProfileForm(original_username=current_user.username,
                          original_email=current_user.email,
                          obj=current_user)
    if form.validate_on_submit():
        # Traitement du formulaire
        current_user.username = form.username.data
        current_user.first_name = form.first_name.data
        current_user.last_name = form.last_name.data
        current_user.email = form.email.data
        current_user.location = form.location.data
        current_user.bio = form.bio.data
        
        if form.profile_picture.data:
            # Traitement de l'image de profil
            filename = secure_filename(form.profile_picture.data.filename)
            # Assurez-vous que le dossier uploads existe
            upload_folder = os.path.join(current_app.config['UPLOAD_FOLDER'], 'profiles')
            os.makedirs(upload_folder, exist_ok=True)
            filepath = os.path.join(upload_folder, filename)
            form.profile_picture.data.save(filepath)
            current_user.profile_picture = filename
            
        db.session.commit()
        flash('Profil mis à jour avec succès!', 'success')
        return redirect(url_for('profile.profile_view'))
        
    return render_template('profile/edit_profile.html', form=form, user=current_user)

@bp.route('/profile/change-password', methods=['GET', 'POST'])
@login_required
def change_password():
    form = ChangePasswordForm()
    if form.validate_on_submit():
        if current_user.check_password(form.current_password.data):
            current_user.set_password(form.new_password.data)
            db.session.commit()
            flash('Mot de passe modifié avec succès!', 'success')
            return redirect(url_for('profile.profile_view'))
        flash('Mot de passe actuel incorrect', 'error')
    return render_template('profile/change_password.html', form=form)

@bp.route('/profile/post/new', methods=['GET', 'POST'])
@login_required
def new_post():
    form = PostForm()
    if form.validate_on_submit():
        post = Post(
            title=form.title.data,
            content=form.content.data,
            user_id=current_user.id
        )
        
        if form.image.data:
            filename = secure_filename(form.image.data.filename)
            filepath = os.path.join(current_app.config['UPLOAD_FOLDER'], 'posts', filename)
            form.image.data.save(filepath)
            post.image_filename = filename
            
        db.session.add(post)
        db.session.commit()
        flash('Post publié avec succès!', 'success')
        return redirect(url_for('profile.profile_view'))
    return render_template('profile/new_post.html', form=form)

@bp.route('/profile/post/<int:post_id>/delete', methods=['POST'])
@login_required
def delete_post(post_id):
    post = Post.query.get_or_404(post_id)
    if post.user_id != current_user.id:
        flash('Vous n\'êtes pas autorisé à supprimer ce post', 'error')
        return redirect(url_for('profile.profile_view'))
    
    db.session.delete(post)
    db.session.commit()
    flash('Post supprimé avec succès!', 'success')
    return redirect(url_for('profile.profile_view')) 