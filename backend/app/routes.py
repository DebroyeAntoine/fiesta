from flask import jsonify, Blueprint, request
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity
from app.models import db, User, Round, Player, bcrypt, PlayerRound, Game
from app.utils.character_loader import load_characters_from_file
from app.socket import socketio
from flask_socketio import emit, join_room, leave_room
import random

CHARACTERS_FILE_PATH = 'app/utils/characters.txt'
characters = load_characters_from_file(CHARACTERS_FILE_PATH)
bp = Blueprint("api", __name__)

@bp.route('/')
def home():
    print("coucou")
    return jsonify({'message': 'Hello from Fiesta de los Muertos!'})

auth_bp = Blueprint('auth', __name__)

@auth_bp.route('/register', methods=['POST'])
def register():
    data = request.get_json()
    username = data.get('username')
    password = data.get('password')

    if not username or not password:
        return jsonify({"message": "Username and password are required."}), 400

    existing_user = User.query.filter_by(username=username).first()
    if existing_user:
        return jsonify({"message": "User already exists."}), 400

    hashed_password = bcrypt.generate_password_hash(password).decode('utf-8')
    new_user = User(username=username, password=hashed_password)
    db.session.add(new_user)
    db.session.commit()

    return jsonify({"message": "User created successfully."}), 201

@auth_bp.route('/delete', methods=['DELETE'])
def delete_all():
    print("delete")
    try:
        db.session.query(User).delete()
        db.session.commit()
        return jsonify({"message": "Tous les utilisateurs ont été supprimés."}), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": str(e)}), 500

def tmp_create_game_and_player(user):
    game = Game.query.filter_by(id=1).first()

    if not game:
        game = Game(id=1, current_round=1)
        db.session.add(game)
        db.session.commit()

        new_round = Round(game_id=game.id, number=1)
        db.session.add(new_round)
        db.session.commit()

    player = Player.query.filter_by(user_id=user.id, game_id=game.id).first()
    if not player:

        used_words = {p.initial_word for p in PlayerRound.query.join(Player).filter(Player.game_id == game.id).all()}
        initial_word = random.choice(characters)

        while initial_word in used_words:
            initial_word  = random.choice(characters)
        player = Player(user_id=user.id, game_id=game.id)
        db.session.add(player)
        db.session.commit()

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
    username = get_jwt_identity()
    join_room(f"game_{game_id}")

    emit('user_joined', {'message': f'User {username} has joined the game'}, room=f"game_{game_id}")

# WebSocket event when a user leaves a game room
@socketio.on('leave_game')
def on_leave_game(data):
    game_id = data['game_id']
    username = get_jwt_identity()
    leave_room(f"game_{game_id}")

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

@game_bp.route('/game/submit_word', methods=['POST'])
@jwt_required()
def submit_word():
    current_player_id = get_jwt_identity()
    data = request.get_json()
    word = data.get('word')
    round_id = data.get('round_id')
    game_id = data.get('game_id')

    player_round = PlayerRound.query.filter_by(player_id=current_player_id, round_id=round_id).first()

    if player_round:
        player_round.word_submitted = word
        db.session.commit()

        socketio.emit('word_submitted', {'player_id': current_player_id})

        submitted_count = PlayerRound.query.filter_by(round_id=round_id).filter(PlayerRound.word_submitted.isnot(None)).count()

        total_players_count = Player.query.filter_by(game_id=game_id).count()

        all_submitted = submitted_count == total_players_count

        if all_submitted:
            emit_new_round_event(game_id, round_id)

        return jsonify({"message": "Word submitted successfully!"}), 200
    else:
        return jsonify({"error": "PlayerRound not found!"}), 404

def emit_new_round_event(round_id, game_id):
    players = Player.query.filter_by(game_id=game_id).all()

    new_words = {}

    submitted_words = PlayerRound.query.filter_by(round_id=round_id).all()

    # fill new words with a rotation of old words
    for index, player in enumerate(players):
        submitted_word = submitted_words[(index + 1) % len(submitted_words)].word_submitted
        new_words[player.id] = submitted_word

        player_round = PlayerRound.query.filter_by(player_id=player.id, round_id=round_id).first()
        if player_round:
            player_round.initial_word = submitted_word

    db.session.commit()

    socketio.emit('new_round', {'round_id': round_id})

def broadcast_player_list(game_id):
    players = Player.query.filter_by(game_id=game_id).all()
    player_data = [{"id": player.id, "username": player.username} for player in players]
    # Emitting to the room corresponding to this game_id
    try:
      socketio.emit('update_player_list', {'players': player_data, 'num_players': len(player_data)})#, room=f"game_{game_id}")
    except Exception as e:
        print(e)

@game_bp.route('/game/<int:game_id>/players', methods=['GET'])
@jwt_required()
def get_players(game_id):
    players = Player.query.filter_by(game_id=game_id).all()

    current_round = Round.query.filter_by(game_id=game_id).order_by(Round.id.desc()).first()

    player_data = []
    for player in players:
        player_round = PlayerRound.query.filter_by(player_id=player.id, round_id=current_round.id).first()
        submitted = player_round.word_submitted is not None if player_round else False

        player_data.append({
            "id": player.id,
            "username": player.username,
            "word_submitted": submitted
        })

    return jsonify({"players": player_data})

@game_bp.route('/game/<int:game_id>/current_round', methods=['GET'])
@jwt_required()
def get_current_round(game_id):
    current_player_id = get_jwt_identity()

    round = Round.query.filter_by(game_id=game_id).order_by(Round.id.desc()).first()
    if not round:
        return jsonify({"error": "No rounds found"}), 404

    player_round = PlayerRound.query.filter_by(round_id=round.id, player_id=current_player_id).first()

    if not player_round:
        return jsonify({"error": "No player round found for the current player"}), 404

    return jsonify({"initial_word": player_round.initial_word})

@game_bp.route('/game/<int:game_id>/advance_round', methods=['POST'])
@jwt_required()
def advance_round(game_id):
    game = Game.query.get_or_404(game_id)

    if game.current_round > 4:
        return jsonify({"message": "Game over"}), 200

    current_round = Round.query.filter_by(game_id=game.id, number=game.current_round).first()
    player_rounds = PlayerRound.query.filter_by(round_id=current_round.id).all()
    players = Player.query.filter_by(game_id=game.id).all()

    if len(player_rounds) < len(players):
        return jsonify({"message": "Not all players have submitted their words"}), 400

    game.current_round += 1
    db.session.commit()

    return jsonify({"message": f"Advanced to Round {game.current_round}"}), 200



