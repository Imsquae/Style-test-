from flask import Blueprint, render_template, request
from flask_login import LoginManager, UserMixin
from app import db
from app.models import Boutique, User
from app.decorators import admin_required
from app.services import get_recent_activities

main = Blueprint('main', __name__)
boutiques = Blueprint('boutiques', __name__)
admin = Blueprint('admin', __name__)

login_manager = LoginManager()
login_manager.login_view = 'auth.login'


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


@main.route('/')
def home():
    # Récupérer les boutiques récentes et populaires
    recent_boutiques = Boutique.query.order_by(Boutique.created_at.desc()).limit(6).all()
    return render_template('home.html', recent_boutiques=recent_boutiques)


@boutiques.route('/search')
def search():
    category = request.args.get('category')
    price_range = request.args.get('price_range')
    target_audience = request.args.get('target_audience')
    
    query = Boutique.query
    
    if category:
        query = query.filter_by(category_id=category)
    if price_range:
        query = query.filter_by(price_range=price_range)
    if target_audience:
        query = query.filter_by(target_audience=target_audience)

    boutiques = query.all()
    return render_template('boutiques/search.html', boutiques=boutiques)


@admin.route('/dashboard')
@admin_required
def dashboard():
    stats = {
        'total_users': User.query.count(),
        'total_boutiques': Boutique.query.count(),
        'recent_activities': get_recent_activities()
    }
    return render_template('admin/dashboard.html', stats=stats)


db.create_all()
