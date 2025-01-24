# app/infrastructure/database/__init__.py
"""
Database infrastructure package
"""
from .session import db
from .base_repository import BaseRepository

__all__ = ['db', 'BaseRepository']
