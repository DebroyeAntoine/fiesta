# app/api/controllers/game_controller.py
from flask import request, jsonify, g
from app.core.services import GameService
from app.core.repositories import UserRepository, PlayerRepository
import random

class GameController:
    def __init__(self):
        self.game_service = GameService()
        self.user_repository = UserRepository()
        self.player_repository = PlayerRepository()

    def get_games(self):
        games = self.game_service.get_waiting_games()
        return jsonify({'games': games}), 200

    def start_game(self, game_id):
        user_id = self._get_user_identity()
        result = self.game_service.start_game(game_id, user_id)
        return result

    def create_game(self, user_id):
        return self.game_service.create_game(user_id)

    def remake_game(self, game_id, user_id, result):
        return self.game_service.remake_game(game_id, user_id, result)

    def quit_game(self, game_id):
        self.game_service.quit_game(game_id)
        return jsonify({'message': "success"}), 200

    def get_lobby(self, game_id):
        user_id = self._get_user_identity()
        game_details = self.game_service.get_lobby_details(game_id, user_id)
        return jsonify(game_details), 200

    def get_players(self, game_id):
        players = self.game_service.get_players_in_game(game_id)
        return jsonify({"players": players})

    def get_game_infos(self, game_id):
        user_id = self._get_user_identity()
        game_info = self.game_service.get_game_details(game_id, user_id)
        return jsonify(game_info), 200

    def get_current_round(self, game_id):
        user_id = self._get_user_identity()
        round_info = self.game_service.get_or_create_current_round(game_id,
                                                                   user_id)
        return jsonify(round_info)

    def submit_word(self):
        user_id = self._get_user_identity()
        data = request.get_json()
        word = data.get('word')
        round_id = data.get('round_id')
        game_id = data.get('game_id')
        return self.game_service.submit_word(user_id, word, round_id, game_id)

    def submit_associations(self, game_id):
        user_id = self._get_user_identity()
        data = request.get_json()
        associations = data['associations']
        return self.game_service.handle_submit_association(game_id, user_id,
                                                            associations)

    def get_word_evolution(self, game_id):
        word_evolution = self.game_service.get_word_evolution(game_id)
        return jsonify({'word_evolution': word_evolution})

    def _get_user_identity(self):
        return int(g.jwt_identity) if hasattr(g, 'jwt_identity') else None

    def join_game(self, user_id, game_id):
        return self.game_service.join_game(user_id, game_id)

    def add_existing_rooms(self, user_id):
        return self.game_service.add_existing_rooms(user_id)
