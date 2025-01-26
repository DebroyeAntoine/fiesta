# app/core/repositories/user_repository.py
from app.domain.entities import User
from app.infrastructure.database import db, BaseRepository

class UserRepository(BaseRepository):
    def __init__(self):
        super().__init__(User)

    def find_by_username(self, username):
        return User.query.filter_by(username=username).first()

    def find_by_user_id(self, user_id):
        return User.query.get(user_id)

    def create(self, username, hashed_password):
        user = User(username=username, password=hashed_password)
        return self.save(user)

    def delete_all(self):
        db.session.query(User).delete()
        db.session.commit()

    def add_room(self, user_id, room):
        user = self.find_by_user_id(user_id)
        rooms = user.get_rooms()
        rooms.append(room)
        user.set_rooms(rooms)
