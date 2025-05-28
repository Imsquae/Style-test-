from flask import Blueprint, render_template
from app.models.boutique import Boutique
from app.extensions import db

bp = Blueprint('main', __name__)

@bp.route('/')
def home():
    recent_boutiques = Boutique.query.order_by(Boutique.created_at.desc()).limit(6).all()
    return render_template('main/home.html', recent_boutiques=recent_boutiques) 