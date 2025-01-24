# app/core/repositories/user_repository.py
from app.domain.entities import User
from app.infrastructure.database import db, BaseRepository

class UserRepository(BaseRepository):
    def __init__(self):
        super().__init__(User)

    def find_by_username(self, username):
        return User.query.filter_by(username=username).first()

    def create(self, username, hashed_password):
        user = User(username=username, password=hashed_password)
        return self.save(user)

    def delete_all(self):
        db.session.query(User).delete()
        db.session.commit()
