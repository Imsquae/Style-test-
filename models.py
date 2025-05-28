from datetime import datetime
from flask_sqlalchemy import SQLAlchemy
from app.models.boutique import Boutique  # Ajout de l'import explicite

db = SQLAlchemy()


class BoutiqueVisit(db.Model):
    __tablename__ = 'boutique_visits'
    id = db.Column(db.Integer, primary_key=True)
    boutique_id = db.Column(db.Integer, db.ForeignKey('boutiques.id'), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=True)  # Nullable pour les visiteurs non connectés
    timestamp = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    
    boutique = db.relationship('Boutique', backref=db.backref('visits', lazy='dynamic'))
    user = db.relationship('User', backref=db.backref('boutique_visits', lazy='dynamic'))


class UserEngagement(db.Model):
    __tablename__ = 'user_engagements'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    boutique_id = db.Column(db.Integer, db.ForeignKey('boutiques.id'), nullable=False)
    action_type = db.Column(db.String(50), nullable=False)  # 'review', 'favorite', etc.
    timestamp = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    
    user = db.relationship('User', backref=db.backref('engagements', lazy='dynamic'))
    boutique = db.relationship('Boutique', backref=db.backref('engagements', lazy='dynamic'))


# Supprimez la définition partielle de Boutique ici car elle est déjà définie dans boutique.py 