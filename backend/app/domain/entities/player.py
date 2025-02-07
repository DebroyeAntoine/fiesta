# app/domain/entities/player.py
from app.infrastructure.database.session import db
from app.domain.entities import User
import json

class Player(db.Model):
    __tablename__ = 'player'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    game_id = db.Column(db.Integer, db.ForeignKey('game.id'), nullable=True)

    def __init__(self, user_id, game_id):
        self.user_id = user_id
        self.game_id = game_id

    @property
    def username(self):
        return User.query.get(self.user_id).username
    player_rounds = db.relationship('PlayerRound', backref='player', lazy=True,
                                    cascade='all, delete-orphan')
    def __repr__(self):
        return f'<Player {self.username} playing as {self.id} with user "\
                "{self.user_id}>'
