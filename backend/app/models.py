# app/models.py
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from sqlalchemy.dialects.postgresql import JSON

db = SQLAlchemy()
bcrypt = Bcrypt()

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password = db.Column(db.String(128), nullable=False)

    # Games where the user is in
    games = db.relationship('Player', backref='user', lazy=True)

    def __repr__(self):
        return f'<User {self.username}>'

# backend/models.py

class PlayerRound(db.Model):
    __tablename__ = 'player_round'
    id = db.Column(db.Integer, primary_key=True)
    round_id = db.Column(db.Integer, db.ForeignKey('round.id'), nullable=False)
    player_id = db.Column(db.Integer, db.ForeignKey('player.id'), nullable=False)
    word_submitted = db.Column(db.String(100), nullable=True)  # word submitted at the end of a round
    initial_word = db.Column(db.String(100), nullable=False)  # Initial word at the beginning of a round

    def __repr__(self):
        return f"<PlayerRound Player {self.player_id}, Round {self.round_id}, InitialWord {self.initial_word},  Word: {self.word_submitted}>"

class Round(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    game_id = db.Column(db.Integer, db.ForeignKey('game.id'), nullable=False)
    number = db.Column(db.Integer, nullable=False)  # TODO remove or use it
    player_rounds = db.relationship('PlayerRound', backref='round', lazy=True)

    def __repr__(self):
        return f"<Round {self.number} in Game {self.game_id}>"

class Game(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    players = db.relationship('Player', backref='game', lazy=True,foreign_keys='Player.game_id')
    rounds = db.relationship('Round', backref='game', lazy=True)
    current_round = db.Column(db.Integer, default=1)
    owner_id = db.Column(db.Integer, db.ForeignKey('player.id'), nullable=False)
    owner = db.relationship(
        'Player',
        foreign_keys=[owner_id],  # Utilise explicitement owner_id pour cette relation
        backref='owned_games'
    )
    constraints = db.Column(JSON, default=list)
    status = db.Column(db.String(20), default='waiting')  # valeurs possibles: waiting, in_progress, ended


class Player(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    game_id = db.Column(db.Integer, db.ForeignKey('game.id'), nullable=True)

    @property
    def username(self):
        return User.query.get(self.user_id).username
    player_rounds = db.relationship('PlayerRound', backref='player', lazy=True)
    def __repr__(self):
        return f'<Player {self.user.username} playing as {self.id} with user {self.user_id}>'


# This class will store the game results
class PlayerAssociation(db.Model):
    __tablename__ = 'player_associations'

    game_id = db.Column(db.Integer, db.ForeignKey('game.id'), primary_key=True)
    player_id = db.Column(db.Integer, db.ForeignKey('player.id'), primary_key=True)
    skull_word = db.Column(db.String, primary_key=True)
    selected_character = db.Column(db.String, nullable=False)
    is_correct = db.Column(db.Boolean, default=False)


class WordEvolution(db.Model):
    __tablename__ = 'word_evolution'
    id = db.Column(db.Integer, primary_key=True)
    game_id = db.Column(db.Integer, db.ForeignKey('game.id'), nullable=False)
    player_id = db.Column(db.Integer, db.ForeignKey('player.id'), nullable=False)
    round_id = db.Column(db.Integer, db.ForeignKey('round.id'), nullable=False)
    word = db.Column(db.String(100), nullable=False)
    character = db.Column(db.String(100), nullable=True)

    def __repr__(self):
        return f"<WordEvolution Player {self.player_id}, Game {self.game_id}, Round {self.round_id}, Word {self.word}>"
