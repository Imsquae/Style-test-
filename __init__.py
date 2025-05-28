from flask import Flask, request, render_template
from flask_login import current_user, LoginManager
from config import Config
from app.extensions import db, login_manager, socketio, migrate
from flask_caching import Cache
from logging.handlers import RotatingFileHandler
import logging
import os
from datetime import datetime
from app.routes import main, auth, admin, api, boutiques, profile, boutique
from app.services.cache_service import cache
from app.services.backup_service import BackupService
from app.error_handlers import setup_logging, register_error_handlers
from flask_wtf.csrf import CSRFProtect


login_manager = LoginManager()
csrf = CSRFProtect()


def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)
    
    # Configuration de l'upload
    app.config['UPLOAD_FOLDER'] = os.path.join(app.static_folder, 'uploads')
    app.config['MAX_CONTENT_LENGTH'] = 5 * 1024 * 1024  # 5MB max
    
    # Créer le dossier d'upload s'il n'existe pas
    if not os.path.exists(app.config['UPLOAD_FOLDER']):
        os.makedirs(app.config['UPLOAD_FOLDER'])
    
    # Initialize extensions
    db.init_app(app)
    login_manager.init_app(app)
    socketio.init_app(app)
    migrate.init_app(app, db)
    cache.init_app(app)
    csrf.init_app(app)
    
    # Setup logging
    setup_logging(app)

    # Register error handlers
    register_error_handlers(app)

    # Initialize backup service
    with app.app_context():
        backup_service = BackupService(app)

    # Configuration du login
    login_manager.login_view = 'auth.login'
    login_manager.login_message = 'Veuillez vous connecter pour accéder à cette page.'
    login_manager.login_message_category = 'info'
    
    # Configuration du dossier d'upload
    app.config['UPLOAD_FOLDER'] = os.path.join(app.static_folder, 'uploads')
    os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)
    
    # Import models after db (database) initialization
    from app.models.boutique import Boutique
    from app.models import BoutiqueStats, UserEngagement, BoutiqueVisit
    from app.models import User

    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get(int(user_id))

    # Register blueprints
    app.register_blueprint(main.bp)
    app.register_blueprint(auth.bp)
    app.register_blueprint(admin.bp, url_prefix='/admin')
    app.register_blueprint(api.bp)
    app.register_blueprint(boutiques.bp)
    app.register_blueprint(profile.bp)
    app.register_blueprint(boutique.bp)

    # Context processors
    @app.context_processor
    def utility_processor():
        def get_unread_notifications_count():
            if current_user.is_authenticated:
                from app.models.notification import Notification
                return Notification.query.filter_by(
                    user_id=current_user.id,
                    read=False
                ).count()
            return 0
        return dict(get_unread_notifications_count=get_unread_notifications_count)

    # Before request
    @app.before_request
    def before_request():
        if current_user.is_authenticated:
            current_user.last_seen = datetime.utcnow()
            db.session.commit()

    @app.before_request
    def block_banned_users():
        if current_user.is_authenticated and getattr(current_user, "is_banned", False):
            # Autoriser seulement la déconnexion et la page bannie
            allowed = [
                'auth.logout', 'auth.banned', 'static'
            ]
            if request.endpoint not in allowed:
                return render_template('auth/banned.html')

    # Ensure upload directories exist
    with app.app_context():
        upload_dir = os.path.join(app.static_folder, 'uploads')
        default_images_dir = os.path.join(app.static_folder, 'images')
        os.makedirs(upload_dir, exist_ok=True)
        os.makedirs(default_images_dir, exist_ok=True)
        
        # Copier l'image de profil par défaut si elle n'existe pas
        default_profile_path = os.path.join(default_images_dir, 'default_profile.jpg')
        if not os.path.exists(default_profile_path):
            # Créer une image de profil par défaut simple
            from PIL import Image, ImageDraw, ImageFont
            img = Image.new('RGB', (200, 200), color='#CCCCCC')
            d = ImageDraw.Draw(img)
            try:
                font = ImageFont.truetype("arial.ttf", 60)
            except:
                font = ImageFont.load_default()
            d.text((100, 100), "?", fill='#FFFFFF', font=font, anchor="mm")
            img.save(default_profile_path)

    return app
