from flask_socketio import emit, join_room, leave_room
from flask import current_app
from app.socket import socketio
from app.utils.decorator import exception_handler
from app.api.controllers import GameController

game_controller = GameController()

def decode_token(token):
    """Helper function pour décoder les tokens dans les websockets"""
    if not token:
        raise ValueError("No token provided")
    return current_app.jwt_manager.verify_token(token)

@socketio.on('create_game')
@exception_handler
def create_game(data):
    user_id = decode_token(data.get('token'))['sub']
    game_controller.create_game(user_id=user_id)

@socketio.on('remake')
@exception_handler
def remake_game(data):
    print("test")
    user_id = decode_token(data.get('token'))['sub']
    result = data['result']
    game_id = data['game_id']
    return game_controller.remake_game(game_id, user_id, result)

@socketio.on('join_game')
@exception_handler
def on_join_game(data):
    game_id = data['game_id']
    user_id = decode_token(data.get('token'))['sub']
    return game_controller.join_game(user_id, game_id)

@socketio.on('start_word_reveal')
@exception_handler
def handle_start_reveal(data):
    game_id = data['game_id']
    socketio.emit('reveal_next_step', 0, room=f"game_{game_id}")

@socketio.on('advance_word_reveal')
@exception_handler
def handle_advance_reveal(data):
    game_id = data['game_id']
    step = data['step']
    socketio.emit('reveal_next_step', step, room=f"game_{game_id}")

@socketio.on('join_room')
@exception_handler
def on_join_room(data):
    user_id = decode_token(data.get('token'))['sub']
    game_controller.add_existing_rooms(user_id)

@socketio.on('leave_game')
@exception_handler
def on_leave_game(data):
    user_id = int(decode_token(data.get('token'))['sub'])
    game_id = data['game_id']
    game_controller.leave_game(user_id, game_id)
