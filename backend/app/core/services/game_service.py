# app/core/services/game_service.py
import random
from flask import jsonify
from flask_socketio import emit, join_room, leave_room
from app.core.repositories import (
    GameRepository, 
    PlayerRepository, 
    RoundRepository, 
    WordEvolutionRepository, 
    UserRepository,
    PlayerAssociationRepository,
    PlayerRoundRepository
)
from app.socket import socketio
from app.utils.loader import load_from_file
from sqlalchemy import func
import random

class GameService:
    def __init__(self):
        self.game_repository = GameRepository()
        self.player_repository = PlayerRepository()
        self.round_repository = RoundRepository()
        self.word_evolution_repository = WordEvolutionRepository()
        self.user_repository = UserRepository()
        self.player_association_repository = PlayerAssociationRepository()
        self.player_round_repository = PlayerRoundRepository()
        self.characters = self._load_characters()
        self.constraints_table = self._load_constraints()

    def _load_characters(self):
        return load_from_file('app/utils/characters.txt')

    def _load_constraints(self):
        return load_from_file('app/utils/constraints.txt')

    def _randomize_constraints(self, length):
        constraints = []
        while len(constraints) < length:
            constraint = random.choice(self.constraints())
            if constraint not in constraints:
                constraints.append(constraint)
        return constraints

    def get_waiting_games(self):
        games = self.game_repository.get_waiting_games()
        return [{
            'id': game.id,
            'name': '',
            'players': [player.user.username for player in game.players],
            'maxPlayers': '8',
            'status': game.status
        } for game in games]

    def start_game(self, game_id, user_id):
        game = self.game_repository.get_game(game_id)
        if game.owner_id == user_id:
            game.status = 'running'
            self.game_repository.save(game)
            socketio.emit('game_started', room=f"game_{game_id}")
            return jsonify({
                "message": "Successfully started game",
                "game_id": game_id
            }), 200
        return jsonify({"message": "Fail to start the game"}), 401

    def create_game(self, user_id, constraints=None):
        new_game = self.game_repository.create_game(owner_id=user_id,
                                                       constraints=constraints)
        self.round_repository.create_round(game_id=new_game.id,
                                                       round=1)
        self.player_repository.create_player(user_id=user_id,
                                                          game_id=new_game.id)
        join_room(f"game_{new_game.id}")
        self.user_repository.add_room(user_id, f"game_{new_game.id}")
        socketio.emit('game_created', {'game_id': new_game.id, 'success': True},
             broadcast=True)

    def remake_game(self, game_id, user_id, result):
        old_game = self.game_repository.get_game(game_id)
        constraints = self.game_repository.get_constraints(old_game)
        if result:
            constraints = self._randomize_constraints(len(constraints) + 1)
        else:
            constraints = self._randomize_constraints(len(constraints))
        self.create_game(user_id, constraints)

    def quit_game(self, game_id):
        socketio.emit('go_to_menu', room=f"game_{game_id}")

    def get_lobby_details(self, game_id, user_id):
        game = self.game_repository.get_game(game_id)
        players = self.player_repository.get_game_players(game_id=game_id)
        player_usernames = [player.user.username for player in players]
        is_owner = game.owner_id == user_id
        return {'players': player_usernames, 'isOwner': is_owner}

    def get_players(self, game_id):
        players = self.player_repository.get_game_players(game_id=game_id)
        current_round =self.round_repository.get_current_round(game_id=game_id)
        player_data = []
        for player in players:
            player_round = self.player_round_repository.get_by_id(
                    player_id=player.id, round_id=current_round.id)
            submitted = (player_round.word_submitted is not None if
                         player_round else False)
            player_data.append({
                "id": player.id,
                "username": player.username,
                "word_submitted": submitted
                })
        return player_data

    def get_game_details(self, game_id, user_id):
        current_player = self.player_repository.get_by_user_id(user_id,
                                                               game_id)
        players = self.player_repository.get_game_players(game_id=game_id)

        current_round =self.round_repository.get_current_round(game_id=game_id)
        game = self.game_repository.get_game(game_id)
        constraints = self.game_repository.get_constraints(game)
        player_data = []
        for player in players:
            player_round = self.player_round_repository.get_by_id(
                    player_id=player.id, round_id=current_round.id)
            submitted = (player_round.word_submitted is not None if
                         player_round else False)
            player_data.append({
                "id": player.id,
                "username": player.username,
                "word_submitted": submitted
                })
        return jsonify({"players": player_data,
                        "round_id": current_round.id,
                        "player_id": current_player.id,
                        "constraints": constraints})

    def get_or_create_current_round(self, game_id, user_id):
        player = self.player_repository.get_by_user_id(user_id, game_id)
        if not player:
            self.player_repository.create_player(user_id=user_id,
                                                 game_id=game_id)
        current_round =self.round_repository.get_current_round(game_id=game_id)
        if not current_round:
            return {"error": "No rounds found"}
        player_round = self.player_round_repository.get_by_id(
                player_id=player.id, round_id=current_round.id)
        if not player_round:
            used_words = {pr.initial_word for pr in
                          self.player_round_repository.get_used_words(game_id)}
            initial_word = random.choice(self.characters)
            while initial_word in used_words:
                initial_word = random.choice(self.characters)

            player_round = self.player_round_repository.create(
                    player_id=player.id,
                    round_id=current_round.id,
                    initial_word=initial_word
                )

            self.word_evolution_repository.create(
                    game_id=game_id,
                    player_id=player.id,
                    round_id=current_round.id,
                    word=initial_word,
                    character=initial_word
                    )
        return {
        "round_number": current_round.number,
        "initial_word": player_round.initial_word
        }

    def submit_word(self, user_id, word, round_id, game_id):
    # Validate player and round
        current_player, current_round, error = self._get_player_and_round(
            user_id, game_id, round_id
        )
        if error:
            return jsonify({"error": error[0]}), error[1]

        # Get and validate player round
        player_round, error = self._get_or_validate_player_round(
            current_player.id, round_id
        )
        if error:
            return jsonify({"error": error[0]}), error[1]

        # Update the submitted word
        player_round.word_submitted = word

        # Handle word evolution
        self._handle_word_evolution(game_id, current_player, round_id,
                                    current_round, word)

        # Commit changes
        self.player_round_repository.save(player_round)

        # Notify clients that word was submitted
        socketio.emit('word_submitted', {'player_id': current_player.id})

        # Check round completion
        self._check_round_completion(round_id, game_id, current_round)

        return jsonify({"message": "Word submitted successfully!"}), 200

    def _get_player_and_round(self, user_id, game_id, round_id):
        current_player = self.player_repository.get_by_user_id(user_id, game_id)
        if not current_player:
            return None, None, ("Player not found", 404)
    
        current_round = self.round_repository.get_round(round_id)
        if not current_round:
            return None, None, ("Round not found", 404)
    
        return current_player, current_round, None
    
    def _get_or_validate_player_round(self, player_id, round_id):
        player_round = self.player_round_repository.get_by_id(
            player_id=player_id,
            round_id=round_id
        )
        if not player_round:
            return None, ("PlayerRound not found", 404)
        return player_round, None
    
    def _handle_word_evolution(self, game_id, current_player, round_id,
                               current_round, word):
        word_evolution = self.word_evolution_repository.get_by_game_player_round(
            game_id, current_player.id, round_id
        )
    
        if word_evolution:
            word_evolution.word = word
        else:
            character = (word if current_round.number == 1 else
                         self._get_previous_character(game_id, current_player,
                                                     current_round))
    
            word_evolution = self.word_evolution_repository.create(
                game_id=game_id,
                player_id=current_player.id,
                round_id=round_id,
                word=word,
                character=character
            )
    
        return word_evolution
    
    def _check_round_completion(self, round_id, game_id, current_round):
        submitted_count = self.player_round_repository.count_submitted(round_id)
        total_players_count = self.player_repository.count_players(game_id)
    
        all_submitted = submitted_count == total_players_count
    
        if all_submitted:
            if current_round.number == 4:
                self._emit_game_over(game_id)
            else:
                self._emit_new_round(round_id, game_id)
