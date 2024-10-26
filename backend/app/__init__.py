# app/__init__.py
from flask import Flask
from flask_cors import CORS
from app.models import db
from app.routes import auth_bp, game_bp,bp
from app.socket import socketio

def create_app():
    app = Flask(__name__)
    CORS(app)

    # Configuration
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    # Initialize db
    db.init_app(app)

    # Register blueprints
    app.register_blueprint(auth_bp)
    app.register_blueprint(game_bp)
    app.register_blueprint(bp)

    # Create the database tables
    with app.app_context():
        db.create_all()

    # Initialize SocketIO
    socketio.init_app(app)

    return app

