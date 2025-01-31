# app/api/__init__.py
"""
API package containing routes and controllers
"""
from .routes import auth_bp, game_bp
from .controllers import AuthController, GameController

__all__ = ['auth_bp', 'AuthController', 'game_bp', 'GameController']
