from app.extensions import db
from datetime import datetime
from app.models.boutique import Boutique


class BoutiqueStats(db.Model):
    __tablename__ = 'boutique_stats'
    id = db.Column(db.Integer, primary_key=True)
    boutique_id = db.Column(db.Integer, db.ForeignKey('boutiques.id'), nullable=False)
    views = db.Column(db.Integer, default=0)
    searches = db.Column(db.Integer, default=0)
    date = db.Column(db.Date, default=datetime.utcnow().date)
    
    boutique = db.relationship(
        Boutique,
        backref=db.backref('stats', lazy='dynamic')
    )


class UserActivity(db.Model):
    __tablename__ = 'user_activities'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    action = db.Column(db.String(50))
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)
    details = db.Column(db.JSON)
    
    user = db.relationship('User', backref=db.backref('activities', lazy='dynamic'))
