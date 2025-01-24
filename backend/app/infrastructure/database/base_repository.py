# app/infrastructure/database/base_repository.py
from app.infrastructure.database.session import db

class BaseRepository:
    def __init__(self, model_class):
        self.model_class = model_class
        self.db = db

    def find_by_id(self, id):
        return self.model_class.query.get(id)

    def save(self, entity):
        self.db.session.add(entity)
        self.db.session.commit()
        return entity

    def delete(self, entity):
        self.db.session.delete(entity)
        self.db.session.commit()

    def delete_all(self):
        self.db.session.query(self.model_class).delete()
        self.db.session.commit()
