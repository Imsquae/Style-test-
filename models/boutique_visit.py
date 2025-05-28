from datetime import datetime
from app.extensions import db


class BoutiqueVisit(db.Model):
    """ """
    __tablename__ = 'boutique_visits'
    id = db.Column(db.Integer, primary_key=True)
    boutique_id = db.Column(db.Integer, db.ForeignKey('boutiques.id'), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=True)
    timestamp = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    
    boutique = db.relationship('Boutique', back_populates='visits')
    user = db.relationship('User', backref=db.backref('boutique_visits', lazy='dynamic')) 