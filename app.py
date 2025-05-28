from flask import Flask
from app.extensions import db, socketio
from config import Config

def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)
    
    # Initialize extensions
    db.init_app(app)
    socketio.init_app(app)
    
    # Register blueprints
    from app.routes import main, auth, admin, api, boutiques, profile, boutique
    app.register_blueprint(main.bp)
    app.register_blueprint(auth.bp)
    app.register_blueprint(admin.bp, url_prefix='/admin')
    app.register_blueprint(api.bp)
    app.register_blueprint(boutiques.bp)
    app.register_blueprint(profile.bp)
    app.register_blueprint(boutique.bp)
    
    return app

app = create_app()

if __name__ == '__main__':
    socketio.run(app, debug=True)





