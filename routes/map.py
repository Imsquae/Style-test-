from flask import Blueprint, render_template, jsonify
from app.models.boutique import Boutique
from app.models.location import Location

bp = Blueprint('map', __name__)


@bp.route('/map')
def show_map():
    return render_template('map/index.html')


@bp.route('/api/boutiques/locations')
def get_boutique_locations():
    boutiques = Boutique.query.join(Location).all()
    
    return jsonify([{
        'id': b.id,
        'name': b.name,
        'latitude': b.location.latitude,
        'longitude': b.location.longitude,
        'address': b.address,
        'category': b.category.name
    } for b in boutiques]) 