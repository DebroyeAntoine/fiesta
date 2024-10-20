# app/models.py
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt

db = SQLAlchemy()
bcrypt = Bcrypt()

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password = db.Column(db.String(128), nullable=False)

    # Relation avec les parties où cet utilisateur est impliqué
    games = db.relationship('Player', backref='user', lazy=True)

    def __repr__(self):
        return f'<User {self.username}>'

# backend/models.py

class PlayerRound(db.Model):
    __tablename__ = 'player_round'
    id = db.Column(db.Integer, primary_key=True)
    round_id = db.Column(db.Integer, db.ForeignKey('round.id'), nullable=False)  # Lien vers le round
    player_id = db.Column(db.Integer, db.ForeignKey('player.id'), nullable=False)  # Lien vers le joueur
    word_submitted = db.Column(db.String(100), nullable=True)  # Le mot soumis par ce joueur
    #character = db.Column(db.String(120), nullable=False)  # Personnage incarné par le joueur
    initial_word = db.Column(db.String(100), nullable=False)  # Mot initial assigné au début de la partie

    def __repr__(self):
        return f"<PlayerRound Player {self.player_id}, Round {self.round_id}, InitialWord {self.initial_word},  Word: {self.word_submitted}>"

# Le modèle Round doit être mis à jour pour ajouter une relation vers PlayerRound
class Round(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    game_id = db.Column(db.Integer, db.ForeignKey('game.id'), nullable=False)
    number = db.Column(db.Integer, nullable=False)  # Le numéro du round (1, 2, 3...)
    player_rounds = db.relationship('PlayerRound', backref='round', lazy=True)  # Les mots soumis par les joueurs

    def __repr__(self):
        return f"<Round {self.number} in Game {self.game_id}>"

class Game(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    players = db.relationship('Player', backref='game', lazy=True)  # Relation avec les joueurs
    rounds = db.relationship('Round', backref='game', lazy=True)  # Relation avec les rounds
    current_round = db.Column(db.Integer, default=1)  # Pour savoir où en est le jeu


class Player(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)  # Lien vers l'utilisateur global
    game_id = db.Column(db.Integer, db.ForeignKey('game.id'), nullable=False)  # Lien vers la partie
    
    @property
    def username(self):
        return User.query.get(self.user_id).username    
    # Relation avec les actions du joueur dans les rounds
    player_rounds = db.relationship('PlayerRound', backref='player', lazy=True)
    def __repr__(self):
        return f'<Player {self.user.username} playing as {self.character}>'
