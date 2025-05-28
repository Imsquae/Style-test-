import requests
from flask import current_app


class GeolocationService:
    def __init__(self):
        self.api_key = current_app.config['MAPS_API_KEY']
        self.base_url = "https://maps.googleapis.com/maps/api/geocode/json"
    
    def get_coordinates(self, address):
        params = {
            'address': f"{address}, Abidjan, Côte d'Ivoire",
            'key': self.api_key
        }
        
        response = requests.get(self.base_url, params=params)
        data = response.json()
        
        if data['status'] == 'OK':
            location = data['results'][0]['geometry']['location']
            return {
                'latitude': location['lat'],
                'longitude': location['lng']
            }
        return None
    
    def get_nearby_boutiques(self, latitude, longitude, radius=5000):
        """Trouve les boutiques dans un rayon donné (en mètres)"""
        from app.models.boutique import Boutique
        from app.models.location import Location

        return Boutique.query.join(Location).filter(
            db.func.st_distance_sphere(
                db.func.point(Location.longitude, Location.latitude),
                db.func.point(longitude, latitude)
            ) <= radius
        ).all() 