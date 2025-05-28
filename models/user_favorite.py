from app.extensions import db

class UserFavorite(db.Model):
    __tablename__ = 'user_favorites'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    boutique_id = db.Column(db.Integer, db.ForeignKey('boutiques.id'), nullable=False)

    user = db.relationship('User')
    boutique = db.relationship('Boutique')

    def __repr__(self):
        return f'<UserFavorite user_id={self.user_id}, boutique_id={self.boutique_id}>' 