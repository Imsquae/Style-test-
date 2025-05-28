from app import db
from datetime import datetime
from flask import url_for
from sqlalchemy import func
from app.models.review import Review


class Boutique(db.Model):
    __tablename__ = 'boutiques'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text)
    address = db.Column(db.String(200))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Clés étrangères
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    category_id = db.Column(db.Integer, db.ForeignKey('categories.id'), nullable=False)
    
    image_filename = db.Column(db.String(255))
    target_audience = db.Column(db.String(50))

    boutique_reviews = db.relationship('Review', back_populates='boutique', lazy='dynamic', cascade='all, delete-orphan')
    visits = db.relationship('BoutiqueVisit', back_populates='boutique', cascade='all, delete-orphan')

    def __repr__(self):
        return f'<Boutique {self.name}>'

    @property
    def average_rating(self):
        """Calcul de la moyenne de notation pour les boutiques"""
        result = db.session.query(func.avg(Review.rating))\
            .filter(Review.boutique_id == self.id)\
            .scalar()
        return float(result) if result else 0.0

    @property
    def reviews_count(self):
        """Get the number of reviews for this boutique"""
        return self.boutique_reviews.count()

    @property
    def image_url(self):
        """Renvoie a l'image de la boutique (default/upload)"""
        if self.image_filename:
            return url_for('static', filename=f'uploads/{self.image_filename}')
        return url_for('static', filename='images/default_boutique.jpg')