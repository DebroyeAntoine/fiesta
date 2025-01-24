# app/domain/entities/word_evolution.py
from app.infrastructure.database.session import db
import json

class WordEvolution(db.Model):
    __tablename__ = 'word_evolution'

    id = db.Column(db.Integer, primary_key=True)
    game_id = db.Column(db.Integer, db.ForeignKey('game.id'), nullable=False)
    player_id = db.Column(db.Integer, db.ForeignKey('player.id'),
                          nullable=False)
    round_id = db.Column(db.Integer, db.ForeignKey('round.id'), nullable=False)
    word = db.Column(db.String(100), nullable=False)
    character = db.Column(db.String(100), nullable=True)

    def __repr__(self):
        return f"<WordEvolution Player {self.player_id}, Game {self.game_id},"\
                " Round {self.round_id}, Word {self.word}>"
