from flask import jsonify, Blueprint, request
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity, decode_token
from app.models import db, User, Round, Player, bcrypt, PlayerRound, Game, PlayerAssociation, WordEvolution
from app.utils.loader import load_from_file
from app.socket import socketio
from flask_socketio import emit, join_room, leave_room
from app.utils.decorator import exception_handler
import random
from sqlalchemy.sql import func
from sqlalchemy.types import  Integer
from sqlalchemy.orm import  aliased

CHARACTERS_FILE_PATH = 'app/utils/characters.txt'
characters = load_from_file(CHARACTERS_FILE_PATH)
CONSTRAINTS_FILE_PATH = 'app/utils/constraints.txt'
constraints_table = load_from_file(CONSTRAINTS_FILE_PATH)
bp = Blueprint("api", __name__)
auth_bp = Blueprint('auth', __name__)
game_bp = Blueprint('game', __name__)

@bp.route('/')
def home():
    print("coucou")
    return jsonify({'message': 'Hello from Fiesta de los Muertos!'})


@auth_bp.route('/register', methods=['POST'])
@exception_handler
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
@exception_handler
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
@exception_handler
def create_game(data):
    try:
        player_id = decode_token(data.get('token'))['sub']

        #FIXME player id instead user id
        new_game = Game(owner_id=player_id, status='waiting')
        constraints = new_game.get_constraints()
        constraints.append("Lettre P")
        new_game.set_constraints(constraints)
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


@game_bp.route('/game/<int:game_id>/remake', methods=['POST'])
@exception_handler
@jwt_required()
def remake_game(game_id):
    player_id = get_jwt_identity()
    try:
        data = request.get_json()
        result = data["result"]
        print(result)
        game = Game.query.get(game_id)

        new_game = Game(owner_id=player_id, status='waiting')
        constraints = game.get_constraints()
        if(result):
            constraints.append("Lettre P")
        if(constraints):
            new_game.set_constraints(constraints)
        db.session.add(new_game)
        db.session.commit()
        new_round = Round(game_id=new_game.id, number=1)
        db.session.add(new_round)

        player = Player(user_id=player_id, game_id=new_game.id)
        db.session.add(player)
        db.session.commit()
        return jsonify({'game_id': new_game.id}), 201


    except Exception as e:
        print(f"Error creating game: {e}")
        return jsonify({"error": "Failed to create game"}), 500


@game_bp.route('/game/get_games', methods=['GET'])
@exception_handler
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

@game_bp.route('/game/<int:game_id>/start', methods=['POST'])
@exception_handler
@jwt_required()
def start_game(game_id):
    player_id = get_jwt_identity()

    game = Game.query.filter_by(id=game_id, status='waiting').first()
    if game.owner_id == player_id:
        game.status = 'running'
        db.session.commit()
        socketio.emit('game_started', room=f"game_{game_id}")

        return jsonify({"message": "Successfully started game", "game_id": game_id}), 200

# WebSocket event when a user joins a game room
@socketio.on('join_game')
@exception_handler
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
    socketio.emit('players_update', {'players': game_players}, room=f"game_{game_id}")

@game_bp.route('/game/<int:game_id>/get_lobby', methods=['GET'])
@exception_handler
@jwt_required()
def get_lobby(game_id):
    game = Game.query.get(game_id)
    current_user_id = get_jwt_identity()
    players = Player.query.filter_by(game_id=game_id).all()

    player_usernames = [player.user.username for player in players]

    is_owner = game.owner_id == current_user_id

    return jsonify({
        'players': player_usernames,
        'isOwner': is_owner
    }), 200

# WebSocket event when a user leaves a game room
@socketio.on('leave_game')
@exception_handler
def on_leave_game(data):
    game_id = data['game_id']
    game = Game.query.get(game_id)
    user_id = decode_token(data.get('player_token'))['sub']
    player = Player.query.filter_by(game_id=game_id, user_id=user_id).first()

    if game and player:
        if game.owner_id == user_id:
            # Get all players execpted the owner
            players = Player.query.filter_by(game_id=game_id).filter(Player.user_id != game.owner_id).all()
            if len(players) > 0:
                game.owner_id = players[0].user_id
                db.session.commit()
                emit('changing_ownership', {}, room=f"game_{game_id}")
            else:
                round = Round.query.filter_by(game_id=game_id).first()
                db.session.delete(round)
                db.session.delete(game)
                db.session.commit()

        db.session.delete(player)
        db.session.commit()
        update_player_list(game_id)
        leave_room(f"game_{game_id}")


@auth_bp.route('/login', methods=['POST'])
@exception_handler
def login():
    data = request.get_json()
    username = data.get('username')
    password = data.get('password')

    user = User.query.filter_by(username=username).first()
    if user and bcrypt.check_password_hash(user.password, password):
        access_token = create_access_token(identity=user.id)
        return jsonify({"message": "Login successful!", 'token': access_token}), 200 #, 'gameId': "1", "roundId":"1", "playerId": str(player.id)}), 200
    else:
        return jsonify({"message": "Invalid username or password."}), 401


@game_bp.route('/game/submit_word', methods=['POST'])
@exception_handler
@jwt_required()
def submit_word():
    user_id = get_jwt_identity()
    data = request.get_json()
    word = data.get('word')
    round_id = data.get('round_id')
    game_id = data.get('game_id')
    current_player_id = Player.query.filter_by(user_id=user_id, game_id=game_id).first().id

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
            current_round_number = Round.query.get(round_id).number
            if current_round_number == 4:
                emit_game_over(game_id)
            else:
                emit_new_round_event(round_id, game_id)

        return jsonify({"message": "Word submitted successfully!"}), 200
    else:
        return jsonify({"error": "PlayerRound not found!"}), 404

def emit_new_round_event(previous_round_id, game_id):
    players = Player.query.filter_by(game_id=game_id).order_by(Player.id).all()

    new_words = {}
    submitted_words = PlayerRound.query.filter_by(round_id=previous_round_id).order_by(PlayerRound.player_id).all()
    previous_round = Round.query.get(previous_round_id)
    new_round = Round(game_id=game_id, number=previous_round.number + 1)
    db.session.add(new_round)
    db.session.commit()

    # fill new words with a rotation of old words
    for index, player in enumerate(players):
        submitted_word = submitted_words[(index - 1) % len(submitted_words)].word_submitted
        new_words[player.id] = submitted_word

        player_round = PlayerRound(player_id=player.id, round_id=new_round.id, initial_word=submitted_word)
        db.session.add(player_round)

    db.session.commit()

    socketio.emit('new_round', {'round_id': new_round.id})

def emit_game_over(game_id):
    game = Game.query.filter_by(id=game_id).first()
    game.status = 'ended'
    db.session.commit()
    initial_words = [
        player_round.initial_word
        for player_round in PlayerRound.query.join(Round)
        .filter(Round.game_id == game_id, Round.number == 1)
        .all()
    ]

    submitted_words = [
        player_round.word_submitted
        for player_round in PlayerRound.query.join(Round)
        .filter(Round.game_id == game_id, Round.number == 4)
        .all()
    ]

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
@exception_handler
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
@exception_handler
@jwt_required()
def get_info(game_id):
    current_player_id = get_jwt_identity()
    current_player = Player.query.filter_by(user_id=current_player_id, game_id=game_id).first()
    players = Player.query.filter_by(game_id=game_id).all()
    current_round = Round.query.filter_by(game_id=game_id).order_by(Round.id.desc()).first()
    game = Game.query.filter_by(id=game_id).first()
    constraints = game.get_constraints()

    player_data = []
    for player in players:
        player_round = PlayerRound.query.filter_by(player_id=player.id, round_id=current_round.id).first()
        submitted = player_round.word_submitted is not None if player_round else False

        player_data.append({
            "id": player.id,
            "username": player.username,
            "word_submitted": submitted
        })

    return jsonify({"players": player_data, "round_id": current_round.id, "player_id": current_player.id, "constraints": constraints})

@game_bp.route('/game/<int:game_id>/current_round', methods=['GET'])
@exception_handler
@jwt_required()
def get_current_round(game_id):
    current_player_id = get_jwt_identity()

    player = Player.query.filter_by(user_id=current_player_id, game_id=game_id).first()
    if not player:
        player = Player(user_id=current_player_id, game_id=game_id)
        db.session.add(player)
        db.session.commit()

    current_round = Round.query.filter_by(game_id=game_id).order_by(Round.number.desc()).first()
    if not current_round:
        return jsonify({"error": "No rounds found"}), 404

    player_round = PlayerRound.query.filter_by(round_id=current_round.id, player_id=player.id).first()
    if not player_round:
        used_words = {p.initial_word for p in PlayerRound.query.join(Player).filter(Player.game_id == game_id).all()}
        initial_word = random.choice(characters)
        while initial_word in used_words:
            initial_word = random.choice(characters)

        player_round = PlayerRound(player_id=player.id, round_id=current_round.id, initial_word=initial_word)
        db.session.add(player_round)

        word_evolution = WordEvolution(game_id=game_id, player_id=player.id, round_id=current_round.id, word=initial_word, character=initial_word)
        db.session.add(word_evolution)
        db.session.commit()

    return jsonify({
        "round_number": current_round.number,
        "initial_word": player_round.initial_word
    })

@game_bp.route('/game/<int:game_id>/submit_associations', methods=['POST'])
@exception_handler
@jwt_required()
def handle_submit_associations(game_id):
    player_id = get_jwt_identity()
    data = request.get_json()
    associations = data['associations']
    game = Game.query.get(game_id)
    if not game:
        return jsonify({"error": "Game not found"}), 404
    is_owner = game.owner_id == player_id

    for association in associations:
        skull_word = association['skull_word']
        selected_character = association['selected_character']

        word_round_4 = aliased(WordEvolution)
        word_round_1 = aliased(WordEvolution)

        round_4 = Round.query.filter_by(game_id=game_id, number=4).first()
        round_1 = Round.query.filter_by(game_id=game_id, number=1).first()

        if round_4 is None or round_1 is None:
            print(f"Erreur : Round 4 ou Round 1 non trouvé pour le jeu {game_id}")
            continue

        # Find the initial character for the skull card
        initial_evolution = db.session.query(word_round_1.character).select_from(word_round_1).join(
            word_round_4,
            (word_round_4.word == skull_word) &
            (word_round_4.round_id == round_4.id) &
            (word_round_4.game_id == game_id) &
            (word_round_4.player_id == word_round_1.player_id)
        ).filter(
            word_round_1.round_id == round_1.id,
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

    return jsonify({"message": "Associations submitted successfully", "isOwner": is_owner}), 200

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

    socketio.emit('game_result', {'result': True if score else False, 'score': sum(scores_dict.values())}, room=f'game_{game_id}')
