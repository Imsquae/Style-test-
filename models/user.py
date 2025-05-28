from datetime import datetime
from app import db
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
from .favorites import favorites
from app.extensions import login_manager
from flask import url_for


class User(db.Model, UserMixin):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(128))
    first_name = db.Column(db.String(64))
    last_name = db.Column(db.String(64))
    bio = db.Column(db.Text)
    profile_picture = db.Column(db.String(255))
    location = db.Column(db.String(100))
    phone_number = db.Column(db.String(20))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    is_active = db.Column(db.Boolean, default=True)
    role = db.Column(db.String(20), default='user')  # user, admin, etc.
    is_confirmed = db.Column(db.Boolean, default=False)
    is_admin = db.Column(db.Boolean, default=False)
    
    # Champs de modération
    is_banned = db.Column(db.Boolean, default=False)
    ban_reason = db.Column(db.Text)
    ban_date = db.Column(db.DateTime)
    warning_count = db.Column(db.Integer, default=0, nullable=False)
    last_warning = db.Column(db.DateTime)
    moderation_notes = db.Column(db.Text)
    
    # Relations
    favorites = db.relationship('Boutique', secondary=favorites,
                              backref=db.backref('favorited_by', lazy='dynamic'))
    reviews = db.relationship('Review', back_populates='reviewer', lazy='dynamic')
    posts = db.relationship('Post', backref='author', lazy='dynamic')
    owned_boutiques = db.relationship('Boutique', 
                                    foreign_keys='Boutique.user_id',
                                    backref=db.backref('owner', lazy='joined'),
                                    lazy='dynamic')

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)
    
    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    @property
    def profile_picture_url(self):
        if self.profile_picture:
            return url_for('static', filename=f'uploads/profiles/{self.profile_picture}')
        return url_for('static', filename='images/default_profile.jpg')

    def __repr__(self):
        return f'<User {self.username}>'

@login_manager.user_loader
def load_user(id):
    return User.query.get(int(id)) 