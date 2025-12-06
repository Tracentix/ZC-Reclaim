from flask import Flask, redirect, url_for
from src.core import db
import os
from src.controllers.auth_controller import auth_bp
from src.controllers.item_controller import item_bp 

def create_app():
    app = Flask(__name__)
    # Config
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///zcreclaim.db'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config['SECRET_KEY'] = 'dev-secret-key'

    db.init_app(app)

    with app.app_context():
        from src.models.user import User
        from src.models.item import Item
        db.create_all()

    app.register_blueprint(auth_bp)
    app.register_blueprint(item_bp)

    @app.route('/')
    def index():
        return redirect(url_for('auth.login'))

    return app

if __name__ == "__main__":
    app = create_app()
    app.run(debug=True)