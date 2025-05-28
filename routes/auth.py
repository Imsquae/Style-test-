from flask import Blueprint, render_template, redirect, url_for, flash, request
from flask_login import login_user, logout_user, login_required, current_user
from app.models import User
from app.forms import LoginForm, RegistrationForm
from app.extensions import db

bp = Blueprint('auth', __name__)


@bp.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        print(f"Attempting login for email: {form.email.data}")  # Debug log
        
        if not user:
            print("User not found")  # Debug log
            flash('Veuillez vérifier vos identifiants et réessayer.', 'error')
            return redirect(url_for('auth.login'))
            
        if not user.check_password(form.password.data):
            print("Invalid password")  # Debug log
            flash('Veuillez vérifier vos identifiants et réessayer.', 'error')
            return redirect(url_for('auth.login'))

        if user.is_banned:
            login_user(user)  # Pour que la classe current_user soit disponible dans le template
            return render_template('auth/banned.html')

        print(f"Login successful for user: {user.username}")  # Debug log
        login_user(user, remember=form.remember_me.data)
        flash('Connexion réussie!', 'success')
        
        next_page = request.args.get('next')
        if not next_page or not next_page.startswith('/'):
            next_page = url_for('main.home')
        return redirect(next_page)

    return render_template('auth/login.html', form=form)


@bp.route('/register', methods=['GET', 'POST'])
def register():
    form = RegistrationForm()
    if form.validate_on_submit():
        user = User(
            email=form.email.data,
            username=form.username.data
        )
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()
        flash('Inscription réussie!', 'success')
        return redirect(url_for('auth.login'))
    return render_template('auth/register.html', form=form)


@bp.route('/logout', methods=['POST'])
@login_required
def logout():
    logout_user()
    flash('Vous avez été déconnecté avec succès.', 'success')
    return redirect(url_for('auth.login'))


@bp.route('/banned')
@login_required
def banned():
    if not current_user.is_banned:
        return redirect(url_for('main.index'))
    return render_template('auth/banned.html') 