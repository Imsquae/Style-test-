from app.extensions import db
from sqlalchemy import Float


class Location(db.Model):
    __tablename__ = 'locations'
    id = db.Column(db.Integer, primary_key=True)
    boutique_id = db.Column(db.Integer, db.ForeignKey('boutiques.id'), nullable=False)
    latitude = db.Column(Float)
    longitude = db.Column(Float)
    commune = db.Column(db.String(100))
    quartier = db.Column(db.String(100))
    
    boutique = db.relationship('Boutique', backref=db.backref('location', uselist=False)) 