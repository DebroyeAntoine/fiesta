# app/core/repositories/player_assocation_repository.py
from sqlalchemy.sql import func
from sqlalchemy.types import  Integer
from app.infrastructure.database.base_repository import db, BaseRepository
from app.domain.entities import PlayerAssociation

class PlayerAssociationRepository(BaseRepository):
    def __init__(self):
        super().__init__(PlayerAssociation)

    def create(self, game_id, player_id, skull_word, selected_character,
               is_correct):
        player_association  = PlayerAssociation(game_id, player_id, skull_word,
                                               selected_character, is_correct)
        return self.save(player_association)

    def count_submitted_players(self, game_id):
        return db.session.query(func.count(
            PlayerAssociation.player_id.distinct())).filter(
                    PlayerAssociation.game_id == game_id).scalar()

    def get_player_scores(self, game_id):
        return PlayerAssociation.query.with_entities(
                PlayerAssociation.player_id,
                func.sum(
                    PlayerAssociation.is_correct.cast(Integer)).label("score")
                ).filter_by(game_id=game_id)\
     .group_by(PlayerAssociation.player_id)\
     .all()
