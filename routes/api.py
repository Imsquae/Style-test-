from flask import Blueprint, jsonify, request, current_app
from flask_login import current_user
from app.models.boutique import Boutique
from app.models.user import User
from functools import wraps
import jwt
from datetime import datetime, timedelta

bp = Blueprint('api', __name__, url_prefix='/api/v1')


def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = request.headers.get('Authorization')
        if not token:
            return jsonify({'message': 'Token manquant'}), 401
            
        try:
            data = jwt.decode(token.split()[1], current_app.config['SECRET_KEY'])
            current_user = User.query.get(data['user_id'])
        except:
            return jsonify({'message': 'Token invalide'}), 401
            
        return f(current_user, *args, **kwargs)
    return decorated


@bp.route('/token', methods=['POST'])
def get_token():
    auth = request.authorization
    if not auth or not auth.username or not auth.password:
        return jsonify({'message': 'Authentification requise'}), 401
        
    user = User.query.filter_by(email=auth.username).first()
    if user and user.check_password(auth.password):
        token = jwt.encode({
            'user_id': user.id,
            'exp': datetime.utcnow() + timedelta(hours=24)
        }, current_app.config['SECRET_KEY'])
        
        return jsonify({'token': token})
    
    return jsonify({'message': 'Identifiants invalides'}), 401


@bp.route('/boutiques', methods=['GET'])
@token_required
def get_boutiques(current_user):
    page = request.args.get('page', 1, type=int)
    per_page = request.args.get('per_page', 10, type=int)
    
    boutiques = Boutique.query.paginate(page=page, per_page=per_page)
    
    return jsonify({
        'boutiques': [{
            'id': b.id,
            'name': b.name,
            'address': b.address,
            'category': b.category.name,
            'price_range': b.price_range
        } for b in boutiques.items],
        'total': boutiques.total,
        'pages': boutiques.pages,
        'current_page': boutiques.page
    })


@bp.route('/boutiques/<int:id>', methods=['GET'])
@token_required
def get_boutique(current_user, id):
    boutique = Boutique.query.get_or_404(id)
    return jsonify({
        'id': boutique.id,
        'name': boutique.name,
        'description': boutique.description,
        'address': boutique.address,
        'category': boutique.category.name,
        'price_range': boutique.price_range,
        'location': {
            'latitude': boutique.location.latitude,
            'longitude': boutique.location.longitude
        } if boutique.location else None
    })


@bp.route('/api/user/boutiques')
@token_required
def get_user_boutiques(current_user):
    boutiques = current_user.owned_boutiques.all()
    return jsonify([{
        'id': b.id,
        'name': b.name,
        'description': b.description,
        'image_url': b.image_url
    } for b in boutiques]) 