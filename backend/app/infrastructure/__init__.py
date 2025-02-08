# app/infrastructure/__init__.py
"""
Infrastructure components package
"""
from .database import db, BaseRepository

__all__ = ['db', 'BaseRepository']
