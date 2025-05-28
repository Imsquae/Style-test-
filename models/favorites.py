from app.extensions import db

favorites = db.Table('favorites',
    db.Column('user_id', db.Integer, db.ForeignKey('users.id'), primary_key=True),
    db.Column('boutique_id', db.Integer, db.ForeignKey('boutiques.id'), primary_key=True)
)
