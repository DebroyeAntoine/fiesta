# app/domain/entities/player_association.py
from app.infrastructure.database.session import db
import json

class PlayerAssociation(db.Model):
    __tablename__ = 'player_association'

    game_id = db.Column(db.Integer, db.ForeignKey('game.id'), primary_key=True)
    player_id = db.Column(db.Integer, db.ForeignKey('player.id'),
                          primary_key=True)
    skull_word = db.Column(db.String, primary_key=True)
    selected_character = db.Column(db.String, nullable=False)
    is_correct = db.Column(db.Boolean, default=False)

    def __init__(self, game_id, player_id, skull_word, selected_character,
                 is_correct):
        self.game_id = game_id
        self.player_id = player_id
        self.skull_word = skull_word
        self.selected_character = selected_character
        self.is_correct = is_correct
