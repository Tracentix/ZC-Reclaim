from flask import Flask, redirect, url_for
from src.core import db
import os
from src.controllers.auth_controller import auth_bp
from src.controllers.item_controller import item_bp 
from src.controllers.claim_controller import claim_bp
from src.controllers.admin_controller import admin_bp

def create_app():
    app = Flask(__name__)
    
    # Absolute path setup for database
    basedir = os.path.abspath(os.path.dirname(__file__))
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'zcreclaim.db')
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config['SECRET_KEY'] = 'dev-secret-key'

    db.init_app(app)

    # Register the admin creation route BEFORE anything else
   # @app.route('/create_admin')
    def create_admin():
        from src.repositories.user_repository import UserRepository
        from werkzeug.security import generate_password_hash
        repo = UserRepository()
        try:
            # Check if admin exists to avoid duplicate error
            existing = repo.get_user_by_email('admin@zewailcity.edu.eg')
            if existing:
                return "Admin already exists. Go to /auth/login"
            
            repo.create_user('admin', 'admin@zewailcity.edu.eg', generate_password_hash('admin123'), role='Admin')
            return "Admin Created Successfully! Go to /auth/login"
        except Exception as e:
            return f"Error: {str(e)}"

    with app.app_context():
        from src.models.user import User
        from src.models.item import Item
        from src.models.claim import Claim 
        db.create_all()

    app.register_blueprint(auth_bp)
    app.register_blueprint(item_bp)
    app.register_blueprint(claim_bp)
    app.register_blueprint(admin_bp)

    @app.route('/')
    def index():
        return redirect(url_for('auth.login'))

    return app

if __name__ == "__main__":
    app = create_app()
    app.run(debug=True)