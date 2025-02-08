# app/core/repositories/player_repository.py
from app.infrastructure.database.base_repository import BaseRepository
from app.domain.entities.player import Player

class PlayerRepository(BaseRepository):
    def __init__(self):
        super().__init__(Player)

    def get_game_players(self, game_id):
        return Player.query.filter_by(game_id=game_id).all()

    def get_game_players_expect_owner(self, game_id, game):
        return Player.query.filter_by(game_id=game_id).filter(
                Player.user_id != game.owner_id).all()

    def create_player(self, user_id, game_id):
        player = Player(user_id, game_id)
        print(player)
        return self.save(player)

    def get_by_user_id(self, user_id, game_id):
        return Player.query.filter_by(user_id=user_id, game_id=game_id).first()

    def count_players(self, game_id):
        return Player.query.filter_by(game_id=game_id).count()

    def get_existing(self, user_id, game_id):
        return Player.query.filter_by(game_id=game_id,user_id=user_id).first()

    def delete_player(self, player):
        self.delete(player)
