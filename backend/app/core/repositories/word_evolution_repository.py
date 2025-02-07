# app/core/repositories/word_evolution_repository.py
from sqlalchemy import select
from app.infrastructure.database.base_repository import db, BaseRepository
from app.domain.entities import WordEvolution, Player, Round, User

class WordEvolutionRepository(BaseRepository):
    def __init__(self):
        super().__init__(WordEvolution)

    # pylint: disable=too-many-arguments too-many-positional-arguments
    def create(self, game_id, player_id, round_id, word, character):
        word_evolution = WordEvolution(game_id=game_id, player_id=player_id,
                                       round_id=round_id, word=word,
                                       character=character)
        return self.save(word_evolution)

    def get_by_game_player_round(self, game_id, player_id, round_id):
        return WordEvolution.query.filter_by(game_id=game_id,
                                             player_id=player_id,
                                             round_id=round_id).first()

    def get_by_word(self, game_id, round_id, word):
        return WordEvolution.query.filter_by(game_id=game_id,
                                             round_id=round_id,
                                             word=word).first()

    def get_evolution_by_game(self, game_id):
        query = (
            select(
                WordEvolution.player_id,
                User.username,
                WordEvolution.word,
                WordEvolution.character,
                Round.number.label('round_number')
            )
            .join(Round, WordEvolution.round_id == Round.id)
            .join(Player, WordEvolution.player_id == Player.id)
            .join(User, Player.user_id == User.id)
            .filter(WordEvolution.game_id == game_id)
            .order_by(WordEvolution.player_id, Round.number)
        )
        return db.session.execute(query).all()

        #return query.all()
