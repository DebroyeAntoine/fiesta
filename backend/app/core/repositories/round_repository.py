# app/core/repositories/round_repository.py
from app.infrastructure.database.base_repository import BaseRepository
from app.domain.entities.round import Round

class RoundRepository(BaseRepository):
    def __init__(self):
        super().__init__(Round)

    def create_round(self, game_id, round_number=1):
        round = Round(game_id=game_id, number=round_number)
        return self.save(round)

    def get_current_round(self, game_id):
        return Round.query.filter_by(game_id=game_id).order_by(
                Round.id.desc()).first()

    def get_round(self, round_id):
        return Round.query.get(round_id)

    def get_previous_round(self, game_id, round_number):
        return Round.query.filter_by(game_id=game_id,
                                     number=round_number - 1).first()

    def get_round_by_number(self, game_id, round_number):
        return Round.query.filter_by(game_id=game_id,
                                     number=round_number).first()
