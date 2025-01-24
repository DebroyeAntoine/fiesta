# app/core/services/auth_service.py
from flask import jsonify
from flask_bcrypt import Bcrypt
from app.core.repositories import UserRepository

bcrypt = Bcrypt()

class AuthService:
    def __init__(self):
        self.user_repository = UserRepository()

    def register_user(self, username, password):
        existing_user = self.user_repository.find_by_username(username)
        print("test")
        if existing_user:
            return jsonify({"message": "User already exists."}), 400

        hashed_password = bcrypt.generate_password_hash(
                password).decode('utf-8')
        return self.user_repository.create(username, hashed_password)

    def authenticate_user(self, username, password):
        user = self.user_repository.find_by_username(username)
        if user and bcrypt.check_password_hash(user.password, password):
            return user
        return None

    def delete_all_users(self):
        try:
            self.user_repository.delete_all()
            return True
        except Exception:
            return False
