# Configuration pour les uploads
UPLOAD_FOLDER = os.path.join(basedir, 'app/static/uploads')
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}
MAX_CONTENT_LENGTH = 16 * 1024 * 1024  # 16MB max file size 