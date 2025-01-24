# app/domain/entities/player_association.py
from app.infrastructure.database.session import db
import json

class PlayerAssociation(db.Model):
    __tablename__ = 'player_associations'

    game_id = db.Column(db.Integer, db.ForeignKey('game.id'), primary_key=True)
    player_id = db.Column(db.Integer, db.ForeignKey('player.id'),
                          primary_key=True)
    skull_word = db.Column(db.String, primary_key=True)
    selected_character = db.Column(db.String, nullable=False)
    is_correct = db.Column(db.Boolean, default=False)
