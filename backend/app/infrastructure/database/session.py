# app/infrastructure/database/session.py
"""
Database session management and configuration
"""
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

def init_db(app):
    """
    Initialize the database with the Flask application
    """
    db.init_app(app)
    
    # Create tables within app context
    with app.app_context():
        db.create_all()
