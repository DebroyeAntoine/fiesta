# app/__init__.py
from flask import Flask
from app.models import db
from app.routes import auth_bp, game_bp,bp
from app.socket import socketio
from app.config.config import AppConfig
from app.security.cors import setup_cors
from app.security.jwt import JWTManager
from functools import wraps


def create_app():
    app = Flask(__name__)

    config = AppConfig.load()

    setup_cors(app, config)
    # Configuration
    app.config['SQLALCHEMY_DATABASE_URI'] = config.database.url
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config['JWT_SECRET_KEY'] = config.security.jwt_secret
    app.config['JWT_ACCESS_TOKEN_EXPIRES'] = config.security.jwt_access_expires

    app.jwt_manager = JWTManager(config.security)

    # Initialize db
    db.init_app(app)

    # Register blueprints
    app.register_blueprint(auth_bp, url_prefix='/auth_api')
    app.register_blueprint(game_bp, url_prefix='/game_api')
    app.register_blueprint(bp)

    # Create the database tables
    with app.app_context():
        db.create_all()

    # Initialize SocketIO
    socketio.init_app(app)

    return app

