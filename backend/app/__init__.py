"""
This module initializes the Flask application, sets up configuration, database,
JWT manager, blueprints, and SocketIO integration.
"""

from flask import Flask
from app.models import db
from app.routes import auth_bp, game_bp, bp
from app.socket import socketio
from app.config.config import AppConfig
from app.security.cors import setup_cors
from app.security.jwt import JWTManager


def create_app():
    """
    Creates and configures the Flask application.

    Returns:
        Flask: The initialized Flask application instance.
    """
    app = Flask(__name__)

    # Load configuration
    config = AppConfig.load()

    # Set up CORS
    setup_cors(app, config)

    # Configuration
    app.config['SQLALCHEMY_DATABASE_URI'] = config.database.url
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config['JWT_SECRET_KEY'] = config.security.jwt_secret
    app.config['JWT_ACCESS_TOKEN_EXPIRES'] = config.security.jwt_access_expires

    # Initialize JWT Manager
    app.jwt_manager = JWTManager(config.security)

    # Initialize database
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
