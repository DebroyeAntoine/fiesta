# app/core/repositories/game_repository.py
from app.infrastructure.database.base_repository import BaseRepository
from app.domain.entities.game import Game

class GameRepository(BaseRepository):
    def __init__(self):
        super().__init__(Game)

    def find_waiting_games(self):
        return Game.query.filter_by(status='waiting').all()

    def create_game(self, owner_id, constraints=None):
        game = Game(owner_id=owner_id)
        if constraints:
            game.set_constraints(constraints)
        return self.save(game)

    def find_game_by_id(self, game_id):
        return Game.query.get(game_id)

    def update_game_status(self, game_id, new_status):
        game = self.find_game_by_id(game_id)
        if game:
            game.status = new_status
            self.save(game)
        return game
