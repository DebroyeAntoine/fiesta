from flask import jsonify, Blueprint, request
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity
from app.models import db, User, Round, Player, bcrypt, PlayerRound, Game
from app.socket import socketio
from flask_socketio import emit, join_room, leave_room
import random
characters = ["test", "test2"]
# Pas besoin de créer une nouvelle instance ici
# app = create_app()  # Cette ligne est à retirer
bp = Blueprint("api", __name__)

@bp.route('/')
def home():
    print("coucou")
    return jsonify({'message': 'Hello from Fiesta de los Muertos!'})

#@bp.route('/submit', methods=['POST'])
#def submit_word():
#    data = request.get_json()
#    word = data.get('word')
#    # Logique pour traiter le mot, par exemple, ajouter à une liste ou valider
#    return jsonify(message=f"Mot '{word}' reçu!")

auth_bp = Blueprint('auth', __name__)

@auth_bp.route('/register', methods=['POST'])
def register():
    data = request.get_json()
    username = data.get('username')
    password = data.get('password')

    # Vérification des données
    if not username or not password:
        return jsonify({"message": "Username and password are required."}), 400

    # Vérifier si l'utilisateur existe déjà
    existing_user = User.query.filter_by(username=username).first()
    if existing_user:
        return jsonify({"message": "User already exists."}), 400

    # Hacher le mot de passe et créer un nouvel utilisateur
    hashed_password = bcrypt.generate_password_hash(password).decode('utf-8')
    new_user = User(username=username, password=hashed_password)
    db.session.add(new_user)
    db.session.commit()

    return jsonify({"message": "User created successfully."}), 201

@auth_bp.route('/delete', methods=['DELETE'])
def delete_all():
    print("delete")
    try:
        # Supprimer tous les utilisateurs
        db.session.query(User).delete()
        db.session.commit()
        return jsonify({"message": "Tous les utilisateurs ont été supprimés."}), 200
    except Exception as e:
        db.session.rollback()  # En cas d'erreur, on annule les changements
        return jsonify({"error": str(e)}), 500

def tmp_create_game_and_player(user):
    # Vérifier si la Game 1 existe déjà
    game = Game.query.filter_by(id=1).first()
    
    if not game:
        # Si la Game 1 n'existe pas encore, on la crée
        game = Game(id=1, current_round=1)
        db.session.add(game)
        db.session.commit()

        # Créer les 4 rounds pour cette partie (ou le nombre souhaité)
        for round_number in range(1, 5):  # Par exemple, 4 rounds
            new_round = Round(game_id=game.id, number=round_number)
            db.session.add(new_round)
        db.session.commit()

    # Ajouter le joueur à cette partie s'il n'est pas déjà dans la game
    player = Player.query.filter_by(user_id=user.id, game_id=game.id).first()
    if not player:
        # Si l'utilisateur n'est pas encore un joueur dans cette partie, on le crée
        #character = random.choice(DEFAULT_WORDS)  # Exemple simple pour choisir un "personnage"
        player = Player(user_id=user.id, game_id=game.id)#, character=character)
        db.session.add(player)
        db.session.commit()

        # Assigner un mot initial pour ce joueur au premier round
        initial_word = "test"  # Mot initial pour le joueur (aléatoire pour le moment)
        first_round = Round.query.filter_by(game_id=game.id, number=1).first()
        player_round = PlayerRound(player_id=player.id, round_id=first_round.id, initial_word=initial_word)
        db.session.add(player_round)
        db.session.commit()
    broadcast_player_list(game.id)
    return player


# WebSocket event when a user joins a game room
@socketio.on('join_game')
def on_join_game(data):
    game_id = data['game_id']
    username = get_jwt_identity()  # Retrieve the current user based on JWT
    join_room(f"game_{game_id}")  # User joins the room specific to their game

    emit('user_joined', {'message': f'User {username} has joined the game'}, room=f"game_{game_id}")

# WebSocket event when a user leaves a game room
@socketio.on('leave_game')
def on_leave_game(data):
    game_id = data['game_id']
    username = get_jwt_identity()  # Retrieve the current user based on JWT
    leave_room(f"game_{game_id}")  # User leaves the room specific to their game

    emit('user_left', {'message': f'User {username} has left the game'}, room=f"game_{game_id}")


@auth_bp.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    username = data.get('username')
    password = data.get('password')

    user = User.query.filter_by(username=username).first()
    if user and bcrypt.check_password_hash(user.password, password):
        access_token = create_access_token(identity=user.id)
        player = tmp_create_game_and_player(user)
        return jsonify({"message": "Login successful!", 'token': access_token, 'gameId': "1", "roundId":"1", "playerId": str(player.id)}), 200
    else:
        return jsonify({"message": "Invalid username or password."}), 401

game_bp = Blueprint('game', __name__)

@game_bp.route('/round/<int:round_id>/player/<int:player_id>/submit_word', methods=['POST'])
@jwt_required()
def submit_word(round_id, player_id):
    round = Round.query.get_or_404(round_id)
    player = Player.query.get_or_404(player_id)

    # Assure que ce joueur fait bien partie de ce jeu
    if player.game_id != round.game_id:
        return jsonify({"message": "Player not in this game"}), 403

    data = request.get_json()
    word = data.get('word')

    if not word:
        return jsonify({"message": "Word is required"}), 400

    # Vérifie si ce joueur a déjà soumis un mot pour ce round
    player_round = PlayerRound.query.filter_by(round_id=round_id, player_id=player_id).first()

    if player_round:
        player_round.word_submitted = word  # Met à jour le mot si déjà soumis
    else:
        # Crée un nouvel enregistrement si ce joueur n'a pas encore soumis de mot
        player_round = PlayerRound(
            round_id=round_id,
            player_id=player_id,
            word_submitted=word
        )
        db.session.add(player_round)

    db.session.commit()

    return jsonify({"message": f"Word submitted by Player {player_id} for Round {round_id}"}), 200

def broadcast_player_list(game_id):
    players = Player.query.filter_by(game_id=game_id).all()
    player_data = [{"id": player.id, "username": player.username} for player in players]
    # Emitting to the room corresponding to this game_id
    try:
      socketio.emit('update_player_list', {'players': player_data, 'num_players': len(player_data)})#, room=f"game_{game_id}")
    except Exception as e:
        print(e)

@game_bp.route('/game/<int:game_id>/players', methods=['GET'])
#@jwt_required
def get_players(game_id):
    print("coucou")
    players = Player.query.filter_by(game_id=game_id).all()
    return jsonify({"players": [{"id": player.id, "username": player.username} for player in players]})

@game_bp.route('/round/<int:round_id>/check_completion', methods=['GET'])
@jwt_required()
def check_round_completion(round_id):
    round = Round.query.get_or_404(round_id)
    player_rounds = PlayerRound.query.filter_by(round_id=round.id).all()

    # Récupère tous les joueurs du jeu actuel
    players = Player.query.filter_by(game_id=round.game_id).all()

    # Vérifie si tous les joueurs ont soumis leurs mots
    if len(player_rounds) == len(players):
        return jsonify({"message": "All players have submitted their words"}), 200
    else:
        return jsonify({"message": "Waiting for more players to submit their words"}), 200

@game_bp.route('/game/<int:game_id>/advance_round', methods=['POST'])
@jwt_required()
def advance_round(game_id):
    game = Game.query.get_or_404(game_id)

    # Vérifie si tous les rounds sont complétés
    if game.current_round > 4:
        return jsonify({"message": "Game over"}), 200

    # Vérifie si tous les joueurs ont soumis leurs mots pour le round en cours
    current_round = Round.query.filter_by(game_id=game.id, number=game.current_round).first()
    player_rounds = PlayerRound.query.filter_by(round_id=current_round.id).all()
    players = Player.query.filter_by(game_id=game.id).all()

    if len(player_rounds) < len(players):
        return jsonify({"message": "Not all players have submitted their words"}), 400

    # Avance au round suivant
    game.current_round += 1
    db.session.commit()

    return jsonify({"message": f"Advanced to Round {game.current_round}"}), 200



