# app/core/repositories/player_round_repository.py
from app.infrastructure.database.base_repository import BaseRepository
from app.domain.entities import PlayerRound, Round

class PlayerRoundRepository(BaseRepository):
    def __init__(self):
        super().__init__(PlayerRound)

    def get_by_id(self, player_id, round_id):
        return PlayerRound.query.filter_by(
            player_id=player_id,
            round_id=round_id
        ).first()

    def create(self, player_id, round_id, initial_word):
        player_round = PlayerRound(player_id=player_id,
                                 round_id=round_id,
                                 initial_word=initial_word)
        return self.save(player_round)

    def count_submitted(self, round_id):
        return PlayerRound.query.filter_by(round_id=round_id)\
            .filter(PlayerRound.word_submitted.isnot(None))\
            .count()

    def get_used_words(self, game_id):
        return PlayerRound.query.join(Round)\
            .filter(Round.game_id == game_id)\
            .all()

    def get_initial_words(self, game_id, round_number):
        return [pr.initial_word for pr in PlayerRound.query.join(Round)
                .filter(Round.game_id == game_id,
                       Round.number == round_number)
                .all()]

    def get_submitted_words(self, game_id, round_number):
        return [pr.word_submitted for pr in PlayerRound.query.join(Round)
                .filter(Round.game_id == game_id,
                       Round.number == round_number)
                .all()]

    def get_submitted_words_by_round(self, round_id):
        return [pr.word_submitted for pr in PlayerRound.query
                .filter_by(round_id=round_id)
                .order_by(PlayerRound.player_id)
                .all()]
