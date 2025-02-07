# app/domain/entities/player_round.py
from app.infrastructure.database.session import db

class PlayerRound(db.Model):
    __tablename__ = 'player_round'

    id = db.Column(db.Integer, primary_key=True)
    round_id = db.Column(db.Integer, db.ForeignKey('round.id'), nullable=False)
    player_id = db.Column(db.Integer, db.ForeignKey('player.id'),
                          nullable=False)
    # Word submitted at the end of a round
    word_submitted = db.Column(db.String(100), nullable=True)
    # Initial word at the beginning of a round
    initial_word = db.Column(db.String(100), nullable=False)

    def __repr__(self):
        return (f"<PlayerRound Player {self.player_id}, Round {self.round_id},"
                f"  InitialWord {self.initial_word},  "
                f"Word: {self.word_submitted}>")
