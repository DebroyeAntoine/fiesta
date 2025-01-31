# app/domain/entities/user.py
import json
from app.infrastructure.database.session import db

class User(db.Model):
    __tablename__ = 'user'

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password = db.Column(db.String(120), nullable=False)
    _rooms = db.Column('room', db.Text, nullable=True, default='[]')

    def get_rooms(self):
        return [] if not self._rooms else json.loads(self._rooms)

    def set_rooms(self, rooms):
        self._rooms = json.dumps(rooms)

    def __repr__(self):
        return f'<User {self.username}>'
