# app/domain/entities/game.py
import json
from app.infrastructure.database.session import db

class Game(db.Model):
    __tablename__ = 'game'

    id = db.Column(db.Integer, primary_key=True)
    players = db.relationship('Player', backref='game', lazy=True,
                              foreign_keys='Player.game_id')
    rounds = db.relationship('Round', backref='game', lazy=True,
                             cascade='all, delete-orphan')
    current_round = db.Column(db.Integer, default=1)
    owner_id = db.Column(db.Integer, db.ForeignKey('player.id'),
                         nullable=False)
    owner = db.relationship(
        'Player',
        foreign_keys=[owner_id],
        backref='owned_games'
    )
    constraints = db.Column(db.Text, default='[]', nullable=True)

    status = db.Column(db.String(20), default='waiting')
    def get_constraints(self):
        # Serialization of the string
        return json.loads(self.constraints) if self.constraints else []

    def set_constraints(self, value):
        # deserealization
        self.constraints = json.dumps(value)
