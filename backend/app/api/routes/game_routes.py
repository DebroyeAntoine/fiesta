# app/api/routes/game_routes.py
from flask import Blueprint
from app.api.controllers import GameController
from app.utils.decorator import exception_handler, jwt_required

game_bp = Blueprint('game', __name__)
game_controller = GameController()

@game_bp.route('/game/get_games', methods=['GET'])
@exception_handler
@jwt_required()
def get_games():
    return game_controller.get_games()

@game_bp.route('/game/<int:game_id>/start', methods=['POST'])
@exception_handler
@jwt_required()
def start_game(game_id):
    return game_controller.start_game(game_id)

#@game_bp.route('/game/<int:game_id>/remake', methods=['POST'])
#@exception_handler
#@jwt_required()
#def remake_game(game_id):
#    return game_controller.remake_game(game_id)
#
@game_bp.route('/game/<int:game_id>/quit', methods=['POST'])
@exception_handler
@jwt_required()
def quit_game(game_id):
    return game_controller.quit_game(game_id)

@game_bp.route('/game/<int:game_id>/get_lobby', methods=['GET'])
@exception_handler
@jwt_required()
def get_lobby(game_id):
    return game_controller.get_lobby(game_id)

@game_bp.route('/game/<int:game_id>/players', methods=['GET'])
@exception_handler
@jwt_required()
def get_players(game_id):
    return game_controller.get_players(game_id)

@game_bp.route('/game/<int:game_id>/get_game_infos', methods=['GET'])
@exception_handler
@jwt_required()
def get_info(game_id):
    return game_controller.get_game_infos(game_id)

@game_bp.route('/game/<int:game_id>/current_round', methods=['GET'])
@exception_handler
@jwt_required()
def get_current_round(game_id):
    return game_controller.get_current_round(game_id)

@game_bp.route('/game/submit_word', methods=['POST'])
@exception_handler
@jwt_required()
def submit_word():
    return game_controller.submit_word()

@game_bp.route('/game/<int:game_id>/submit_associations', methods=['POST'])
@exception_handler
@jwt_required()
def submit_associations(game_id):
    return game_controller.submit_associations(game_id)

@game_bp.route('/game/<int:game_id>/word_evolution', methods=['GET'])
@exception_handler
@jwt_required()
def get_word_evolution(game_id):
    return game_controller.get_word_evolution(game_id)
