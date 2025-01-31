# app/domain/entities/round.py
from app.infrastructure.database.session import db
import json

class Round(db.Model):
    __tablename__ = 'round'

    id = db.Column(db.Integer, primary_key=True)
    game_id = db.Column(db.Integer, db.ForeignKey('game.id'), nullable=False)
    number = db.Column(db.Integer, nullable=False)
    player_rounds = db.relationship('PlayerRound', backref='round', lazy=True,
                                    cascade='all, delete-orphan')

    def __repr__(self):
        return f"<Round {self.number} in Game {self.game_id}>"
