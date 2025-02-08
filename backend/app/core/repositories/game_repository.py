# app/core/repositories/game_repository.py
from app.infrastructure.database.base_repository import BaseRepository
from app.domain.entities.game import Game

class GameRepository(BaseRepository):
    def __init__(self):
        super().__init__(Game)

    def get_waiting_games(self):
        return Game.query.filter_by(status='waiting').all()

    def create_game(self, owner_id, constraints=None):
        game = Game(owner_id=owner_id)
        if constraints:
            game.set_constraints(constraints)
        return self.save(game)

    def get_game(self, game_id):
        return Game.query.get(game_id)

    def update_game_status(self, game_id, new_status):
        game = self.get_game(game_id)
        if game:
            game.status = new_status
            self.save(game)
        return game

    def get_constraints(self, game_id):
        game = self.get_game(game_id)
        return game.get_constraints()

    def end_game(self, game_id):
        game = self.get_game(game_id)
        game.status = "ended"
        self.save(game)

    def set_owner(self, game_id, future_owner):
        game = self.get_game(game_id)
        game.owner_id = future_owner
        self.save(game)

    def set_status(self, game_id, status):
        game = self.get_game(game_id)
        game.status = status
        self.save(game)
