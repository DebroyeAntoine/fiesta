# app/api/routes/__init__.py
"""
Routes package initialization.
Exports all blueprints and provides blueprint registration functionality.
"""
from flask import Flask
from .auth_routes import auth_bp

__all__ = [
    'auth_bp',
    'register_blueprints'
]

def register_blueprints(app: Flask) -> None:
    """
    Register all application blueprints with their respective URL prefixes.
    
    Args:
        app: Flask application instance
    """
    app.register_blueprint(auth_bp, url_prefix='/auth_api')
