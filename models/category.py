from app import db
from datetime import datetime


class Category(db.Model):
    __tablename__ = 'categories'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), unique=True, nullable=False)
    description = db.Column(db.Text)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    # Commentons temporairement la colonne updated_at
    # updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relation avec les boutiques - avec backref
    boutiques = db.relationship('Boutique',
                              backref=db.backref('category', lazy='joined'),
                              lazy='dynamic')
    
    def __repr__(self):
        return f'<Category {self.name}>' 