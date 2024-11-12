from flask import jsonify, Blueprint, request
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity, decode_token
from app.models import db, User, Round, Player, bcrypt, PlayerRound, Game, PlayerAssociation, WordEvolution
from app.utils.character_loader import load_characters_from_file
from app.socket import socketio
from flask_socketio import emit, join_room, leave_room
import random
from sqlalchemy.sql import func
from sqlalchemy.types import  Integer
from sqlalchemy.orm import  aliased

CHARACTERS_FILE_PATH = 'app/utils/characters.txt'
characters = load_characters_from_file(CHARACTERS_FILE_PATH)
bp = Blueprint("api", __name__)
auth_bp = Blueprint('auth', __name__)
game_bp = Blueprint('game', __name__)

@bp.route('/')
def home():
    print("coucou")
    return jsonify({'message': 'Hello from Fiesta de los Muertos!'})


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


@socketio.on('create_game')
def create_game(data):
    try:
        player_id = decode_token(data.get('token'))['sub']

        new_game = Game(owner_id=player_id, status='waiting')
        db.session.add(new_game)
        db.session.commit()

        new_round = Round(game_id=new_game.id, number=1)
        db.session.add(new_round)

        player = Player(user_id=player_id, game_id=new_game.id)
        db.session.add(player)
        db.session.commit()

        join_room(f"game_{new_game.id}")
        emit('game_created', {'game_id': new_game.id, 'success': True}, broadcast=True)

    except Exception as e:
        print(f"Error creating game: {e}")
        return jsonify({"error": "Failed to create game"}), 500


@game_bp.route('/game/get_games', methods=['GET'])
@jwt_required()
def get_games():
    games = Game.query.filter_by(status='waiting').all()
    games_list = [{
        'id': game.id,
        'name': '',
        'players': [player.user.username for player in game.players],
        'maxPlayers': '8',
        'status': game.status
    } for game in games]
    return jsonify({'games': games_list}), 201

@game_bp.route('/game/<int:game_id>/join', methods=['POST'])
@jwt_required()
def join_game(game_id):
    player_id = get_jwt_identity()

    game = Game.query.filter_by(id=game_id, status='waiting').first()
    if not game:
        return jsonify({"error": "Game not available or already in progress"}), 404

    player = Player(user_id=player_id, game_id=game_id)
    db.session.add(player)
    db.session.commit()

    join_room(f"game_{game.id}")
    return jsonify({"message": "Successfully joined game", "game_id": game_id}), 200

@game_bp.route('/game/<int:game_id>/start', methods=['POST'])
@jwt_required()
def start_game(game_id):
    player_id = get_jwt_identity()

    game = Game.query.filter_by(id=game_id, status='waiting').first()
    if game.owner_id == player_id:
        game.status = 'running'
        new_round = Round(game_id=game.id, number=1)
        db.session.add(new_round)
        db.session.commit()
        socketio.emit('game_started', room=f"game_{game_id}")

        return jsonify({"message": "Successfully started game", "game_id": game_id}), 200

def create_player(player_id, game_id):
    player = Player.query.filter_by(user_id=player_id, game_id=game_id).first()
    if not player:

        used_words = {p.initial_word for p in PlayerRound.query.join(Player).filter(Player.game_id == game_id).all()}
        initial_word = random.choice(characters)

        while initial_word in used_words:
            initial_word  = random.choice(characters)
        player = Player(user_id=player.id, game_id=game_id)
        db.session.add(player)
        db.session.commit()

        first_round = Round.query.filter_by(game_id=game_id, number=1).first()
        player_round = PlayerRound(player_id=player_id, round_id=first_round.id, initial_word=initial_word)
        word_evolution = WordEvolution(game_id=game_id, player_id=player_id, round_id=first_round.id, word=initial_word, character=initial_word)
        db.session.add(player_round)
        db.session.add(word_evolution)
        db.session.commit()
    #Maybe useless TODO check it
    broadcast_player_list(game_id)
    db.session.commit()


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
        word_evolution = WordEvolution(game_id=game.id, player_id=player.id, round_id=first_round.id, word=initial_word, character=initial_word)
        db.session.add(player_round)
        db.session.add(word_evolution)
        db.session.commit()
    broadcast_player_list(game.id)
    return player


# WebSocket event when a user joins a game room
@socketio.on('join_game')
def on_join_game(data):
    game_id = data['game_id']
    user_id = decode_token(data.get('token'))['sub']
    username = User.query.filter_by(id = user_id).first().username
    player = Player(user_id=user_id, game_id=game_id)
    db.session.add(player)
    db.session.commit()
    join_room(f"game_{game_id}")

    update_player_list(game_id)

    emit('player_joined', {'player': username}, room=f"game_{game_id}")


def update_player_list(game_id):
    game_players = []
    players = Player.query.filter_by(game_id=game_id).all()
    for player in players:
        game_players.append(User.query.get(player.user_id).username)
    print(game_players)
    socketio.emit('players_update', game_players, room=f"game_{game_id}")

@game_bp.route('/game/<int:game_id>/get_lobby', methods=['GET'])
@jwt_required()
def get_lobby(game_id):
    # Récupère le jeu et l'utilisateur actuel via JWT
    game = Game.query.get(game_id)
    current_user_id = get_jwt_identity()
    players = Player.query.filter_by(game_id=game_id).all()

    # Prépare la liste des noms d'utilisateur uniquement
    player_usernames = [player.user.username for player in players]

    # Vérifie si l'utilisateur actuel est le propriétaire de la partie
    is_owner = any(player.id == game.owner_id and player.user_id == current_user_id for player in players)

    return jsonify({
        'players': player_usernames,  # Liste des usernames seulement
        'isOwner': is_owner  # Vrai ou faux seulement pour l'utilisateur actuel
    }), 200
# WebSocket event when a user leaves a game room
@socketio.on('leave_game')
def on_leave_game(data):
    game_id = data['game_id']
    game = Game.query.get(game_id)
    user_id = decode_token(data.get('token'))['sub']
    game.remove(user_id)
    db.commit()
    leave_room(f"game_{game_id}")

    #emit('user_left', {'message': f'User {username} has left the game'}, room=f"game_{game_id}")


@auth_bp.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    username = data.get('username')
    password = data.get('password')

    user = User.query.filter_by(username=username).first()
    if user and bcrypt.check_password_hash(user.password, password):
        access_token = create_access_token(identity=user.id)
        #player = tmp_create_game_and_player(user)
        return jsonify({"message": "Login successful!", 'token': access_token}), 200 #, 'gameId': "1", "roundId":"1", "playerId": str(player.id)}), 200
    else:
        return jsonify({"message": "Invalid username or password."}), 401


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
        word_evolution = WordEvolution.query.filter_by(
            game_id=game_id,
            player_id=current_player_id,
            round_id=round_id
        ).first()

        if word_evolution:
            word_evolution.word = word
        else:
            word_evolution = WordEvolution(game_id=game_id, player_id=current_player_id, round_id=round_id, word=word)
            db.session.add(word_evolution)
        db.session.commit()

        socketio.emit('word_submitted', {'player_id': current_player_id})

        submitted_count = PlayerRound.query.filter_by(round_id=round_id).filter(PlayerRound.word_submitted.isnot(None)).count()

        total_players_count = Player.query.filter_by(game_id=game_id).count()

        all_submitted = submitted_count == total_players_count

        if all_submitted:
            if round_id == 4:
                emit_game_over(game_id)
            else:
                emit_new_round_event(round_id, game_id)

        return jsonify({"message": "Word submitted successfully!"}), 200
    else:
        return jsonify({"error": "PlayerRound not found!"}), 404

def emit_new_round_event(previous_round_id, game_id):
    players = Player.query.filter_by(game_id=game_id).all()

    new_words = {}

    submitted_words = PlayerRound.query.filter_by(round_id=previous_round_id).all()

    new_round = Round(game_id=game_id, number=Round.query.filter_by(game_id=game_id).count() + 1)
    db.session.add(new_round)
    db.session.commit()

    # fill new words with a rotation of old words
    for index, player in enumerate(players):
        submitted_word = submitted_words[(index + 1) % len(submitted_words)].word_submitted
        new_words[player.id] = submitted_word

        player_round = PlayerRound(player_id=player.id, round_id=new_round.id, initial_word=submitted_word)
        db.session.add(player_round)

    db.session.commit()

    socketio.emit('new_round', {'round_id': new_round.id})

def emit_game_over(game_id):
    initial_words = [player_round.initial_word for player_round in PlayerRound.query.filter_by(round_id=1).all()]
    submitted_words = [player_round.word_submitted for player_round in PlayerRound.query.filter_by(round_id=4).all()]
    words_to_sent = initial_words[:]

    while len(words_to_sent) < 8:
        random_word = random.choice(characters)
        if random_word not in words_to_sent:
            words_to_sent.append(random_word)

    random.shuffle(words_to_sent)
    socketio.emit('game_over', {'initial_words': words_to_sent, 'end_words': submitted_words})

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


@game_bp.route('/game/<int:game_id>/get_game_infos', methods=['GET'])
@jwt_required()
def get_info(game_id):
    current_player_id = get_jwt_identity()
    create_player(current_player_id, game_id)
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

    return jsonify({"players": player_data, "round_id": current_round.id, "player_id": current_player_id})

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


@game_bp.route('/game/<int:game_id>/submit_associations', methods=['POST'])
@jwt_required()
def handle_submit_associations(game_id):
    player_id = get_jwt_identity()
    data = request.get_json()
    associations = data['associations']

    for association in associations:
        skull_word = association['skull_word']
        selected_character = association['selected_character']

        word_round_4 = aliased(WordEvolution)
        word_round_1 = aliased(WordEvolution)

        # Find the initial character for the skull card
        initial_evolution = db.session.query(word_round_1.character).select_from(word_round_1).join(
            word_round_4,
            (word_round_4.word == skull_word) &
            (word_round_4.round_id == 4) &
            (word_round_4.game_id == game_id) &
            (word_round_4.player_id == word_round_1.player_id)
        ).filter(
            word_round_1.round_id == 1,
            word_round_1.game_id == game_id
        ).first()
        if initial_evolution is None:
            print(f"Erreur : Aucun mot initial trouvé pour le skull_word {skull_word} du joueur {player_id}")
            continue

        initial_character = initial_evolution[0]
        is_correct = initial_character == selected_character

        new_association = PlayerAssociation(
            game_id=game_id,
            player_id=player_id,
            skull_word=skull_word,
            selected_character=selected_character,
            is_correct=is_correct
        )
        db.session.add(new_association)

    db.session.commit()
    all_submitted = check_all_players_submitted(game_id)

    if all_submitted:
        calculate_scores_and_notify(game_id)

    return jsonify({"message": "Associations submitted successfully"}), 200

def check_all_players_submitted(game_id):
    game = Game.query.get(game_id)
    total_players = len(game.players)

    submitted_players_count = db.session.query(PlayerAssociation.player_id).filter_by(game_id=game_id).distinct().count()

    return total_players == submitted_players_count

def calculate_scores_and_notify(game_id):
    game = Game.query.get(game_id)
    total_players = len(game.players)

    score_to_do = (total_players - 1) * total_players

    player_scores = db.session.query(
        PlayerAssociation.player_id,
        func.sum(PlayerAssociation.is_correct.cast(Integer)).label("score")
    ).filter_by(game_id=game_id).group_by(PlayerAssociation.player_id).all()

    scores_dict = {player_id: score or 0 for player_id, score in player_scores}
    score = sum(scores_dict.values()) >= score_to_do

    socketio.emit('game_result', {'result': "success" if score else "fail", 'score': sum(scores_dict.values())})
