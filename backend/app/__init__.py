from app.models import db
from app.routes import auth_bp, game_bp

from flask import Flask

from flask_cors import CORS

def create_app():
    app = Flask(__name__)
    CORS(app)
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'  # Changez cela selon votre base de données
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    db.init_app(app)
    app.register_blueprint(auth_bp)
    app.register_blueprint(game_bp)
    with app.app_context():
        db.create_all()

    from .routes import bp  # Importer les routes
    app.register_blueprint(bp)
    return app

