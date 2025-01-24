# app/domain/entities/player.py
from app.infrastructure.database.session import db
import json

class Player(db.Model):
    __tablename__ = 'player'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    game_id = db.Column(db.Integer, db.ForeignKey('game.id'), nullable=True)

    @property
    def username(self):
        return User.query.get(self.user_id).username
    player_rounds = db.relationship('PlayerRound', backref='player', lazy=True,
                                    cascade='all, delete-orphan')
    def __repr__(self):
        return f'<Player {self.user.username} playing as {self.id} with user "\
                "{self.user_id}>'
