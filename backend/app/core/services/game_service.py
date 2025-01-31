# app/core/services/game_service.py
import random
from flask import jsonify
from sqlalchemy import func
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
            constraint = random.choice(self.constraints_table)
            if constraint not in constraints:
                constraints.append(constraint)
        return constraints

    def get_waiting_games(self):
        games = self.game_repository.get_waiting_games()
        return [{
            'id': game.id,
            'name': '',
            'players': [player.username for player in game.players],
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

    def create_game(self, user_id, constraints=None, remake=False):
        print("111")
        new_game = self.game_repository.create_game(owner_id=user_id,
                                                       constraints=constraints)
        print("112")
        self.round_repository.create_round(game_id=new_game.id,
                                           round_number=1)
        self.player_repository.create_player(user_id=user_id,
                                         game_id=new_game.id)
        join_room(f"game_{new_game.id}")
        print("113")
        print(new_game.id)
        self.user_repository.add_room(user_id, f"game_{new_game.id}")
        print("114")
        if not remake:
            emit('game_created',
                 {'game_id': new_game.id, 'success': True},broadcast=True)
            print("115")
            return jsonify({"success": True, "game_id": new_game.id}), 200
        else:
            return {"success": True, "game_id": new_game.id}


    def remake_game(self, game_id, user_id, result):
        constraints = self.game_repository.get_constraints(game_id)
        if result:
            constraints = self._randomize_constraints(len(constraints) + 1)
        else:
            constraints = self._randomize_constraints(len(constraints))
        create = self.create_game(user_id, constraints, True)
        print(create)
        socketio.emit('new_game', {'game_id': create['game_id']},
                      room=f"game_{game_id}")

    def quit_game(self, game_id):
        socketio.emit('go_to_menu', room=f"game_{game_id}")

    def get_lobby_details(self, game_id, user_id):
        game = self.game_repository.get_game(game_id)
        players = self.player_repository.get_game_players(game_id=game_id)
        print(players)
        player_usernames = [player.username for player in players]
        #player_usernames = [player.user.username for player in players]
        is_owner = game.owner_id == user_id
        return {'players': player_usernames, 'isOwner': is_owner}

    def get_players_in_game(self, game_id):
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
        constraints = self.game_repository.get_constraints(game_id)
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
        return {"players": player_data,
                "round_id": current_round.id,
                "player_id": current_player.id,
                "constraints": constraints}

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
        word_evolution = (
                self.word_evolution_repository.get_by_game_player_round(
                    game_id, current_player.id, round_id))

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
        submitted_count = self.player_round_repository.count_submitted(
                round_id
                )
        total_players_count = self.player_repository.count_players(game_id)

        all_submitted = submitted_count == total_players_count

        if all_submitted:
            if current_round.number == 4:
                self._emit_game_over(game_id)
            else:
                self._emit_new_round(round_id, game_id)

    def _get_previous_character(self, game_id, current_player, current_round):
        # Get ordered list of players
        players = self.player_repository.get_game_players(game_id)
        player_count = len(players)

        # Find current player's position and previous player
        current_player_index = next(
            i for i, p in enumerate(players) if p.id == current_player.id
        )
        previous_player_index = (current_player_index - 1) % player_count
        previous_player = players[previous_player_index]

        # Get previous round
        previous_round = self.round_repository.get_previous_round(
            game_id, current_round.number
        )

        if not previous_round:
            return None

        # Get previous player's WordEvolution
        previous_word_evolution = (
                self.word_evolution_repository.get_by_game_player_round(
            game_id, previous_player.id, previous_round.id
            )
                )

        return (previous_word_evolution.character if previous_word_evolution
                else None)

    def _emit_game_over(self, game_id):
        self.game_repository.end_game(game_id)
        initial_words = self.player_round_repository.get_initial_words(
                game_id,round_number=1)

        # Get final words from round 4
        submitted_words = self.player_round_repository.get_submitted_words(
                game_id, round_number=4)

        # Prepare words to send (fill with random characters if needed)
        words_to_send = initial_words[:]
        while len(words_to_send) < 8:
            random_word = random.choice(self.characters)
            if random_word not in words_to_send:
                words_to_send.append(random_word)

        random.shuffle(words_to_send)
        socketio.emit('game_over', {
            'initial_words': words_to_send,
            'end_words': submitted_words
            })

    def _emit_new_round(self, previous_round_id, game_id):
        # Get players in order
        players = self.player_repository.get_game_players(game_id)

        # Get submitted words from previous round
        submitted_words = (
                self.player_round_repository.get_submitted_words_by_round(
                    previous_round_id)
                )

        # Create new round
        previous_round = self.round_repository.get_round(previous_round_id)
        new_round = self.round_repository.create_round(
            game_id=game_id,
            round_number=previous_round.number + 1
        )

        # Rotate words between players
        for index, player in enumerate(players):
            submitted_word = submitted_words[(index - 1) % len(
                submitted_words)]

            # Create player round with rotated word
            self.player_round_repository.create(
                player_id=player.id,
                round_id=new_round.id,
                initial_word=submitted_word
            )

        socketio.emit('new_round', {'round_id': new_round.id})

    def handle_submit_association(self, game_id, user_id, associations):
        game = self.game_repository.get_game(game_id)
        if not game:
            return jsonify({"error": "Game not found"}), 404

        is_owner = game.owner_id == user_id

        try:
            # Get rounds 1 and 4
            round_1 = self.round_repository.get_round_by_number(game_id, 1)
            round_4 = self.round_repository.get_round_by_number(game_id, 4)

            if not round_1 or not round_4:
                return jsonify({"error": "Required rounds not found"}), 400

            # Process each association
            for association in associations:
                skull_word = association['skull_word']
                selected_character = association['selected_character']

                # Find the WordEvolution entry for this final word
                final_word_evolution = (
                        self.word_evolution_repository.get_by_word(
                            game_id, round_4.id, skull_word))

                if not final_word_evolution:
                    continue

                # Get the original character
                original_character = final_word_evolution.character
                if not original_character:
                    continue

                player = self.player_repository.get_by_user_id(user_id,
                                                               game_id)
                # Create association record
                self.player_association_repository.create(
                    game_id=game_id,
                    player_id=player.id,
                    skull_word=skull_word,
                    selected_character=selected_character,
                    is_correct=original_character.lower() == selected_character.lower()
                )

            # Check if all players have submitted
            if self.check_all_players_submitted(game_id):
                self.calculate_scores_and_notify(game_id)

            return jsonify({
                "message": "Associations submitted successfully",
                "isOwner": is_owner
            }), 200

        except Exception as e:
            return jsonify({"error": str(e)}), 500

    def check_all_players_submitted(self, game_id):
        game = self.game_repository.get_game(game_id)
        total_players = len(game.players)

        submitted_players_count = (
                self.player_association_repository.count_submitted_players(
                    game_id))

        return total_players == submitted_players_count

    def calculate_scores_and_notify(self, game_id):
        game = self.game_repository.get_game(game_id)
        total_players = len(game.players)

        score_to_do = (total_players - 1) * total_players

        player_scores = self.player_association_repository.get_player_scores(
                game_id)

        scores_dict = {player_id: score or 0 for player_id,
                       score in player_scores}
        score = sum(scores_dict.values()) >= score_to_do

        socketio.emit('game_result', {
            'result': bool(score),
            'score': sum(scores_dict.values())
        }, room=f'game_{game_id}')

    def get_word_evolution(self, game_id):
        word_evolution = self.word_evolution_repository.get_evolution_by_game(
                game_id)

        evolution_data = [{
            'player_id': entry.player_id,
            'username': entry.username,
            'word': entry.word,
            'character': entry.character,
            'round_number': entry.round_number
        } for entry in word_evolution]

        return evolution_data

    def join_game(self, user_id, game_id):
        existing_player = self.player_repository.get_existing(user_id, game_id)
        user = self.user_repository.find_by_user_id(user_id)

        if not existing_player:
            self.player_repository.create_player(user_id, game_id)
            self._update_player_list(game_id)
        print("coucou")

        join_room(f"game_{game_id}")
        self.user_repository.add_room(user.id, f"game_{game_id}")
        emit('player_joined', {'player': user.username},
             room=f"game_{game_id}")

    def _update_player_list(self, game_id):
        game_players = []
        players = self.player_repository.get_game_players(game_id)
        for player in players:
            game_players.append(self.user_repository.find_by_user_id
                                (player.user_id).username)

        socketio.emit('players_update', {'players': game_players},
                      room=f"game_{game_id}")

    def add_existing_rooms(self, user_id):
        rooms = self.user_repository.get_rooms(user_id)
        print(f"rooms {rooms}")
        for room in rooms:
            join_room(room)

