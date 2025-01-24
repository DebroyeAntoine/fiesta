# app/api/controllers/auth_controller.py
from flask import request, jsonify, current_app
from app.core.services import AuthService

class AuthController:
    def __init__(self):
        self.auth_service = AuthService()

    def register(self):
        data = request.get_json()
        username = data.get('username')
        password = data.get('password')

        if not username or not password:
            return jsonify(
                    {"message": "Username and password are required."}), 400

        result = self.auth_service.register_user(username, password)
        if isinstance(result, tuple) and result[1] == 400:
            return result

        token_pair = current_app.jwt_manager.create_token_pair(result.id)
        return jsonify({
            "message": "User created successfully.",
            'token': token_pair.access_token,
            'refresh_token': token_pair.refresh_token
        }), 200

    def login(self):
        data = request.get_json()
        username = data.get('username')
        password = data.get('password')

        user = self.auth_service.authenticate_user(username, password)
        if not user:
            return jsonify({"message": "Invalid username or password."}), 401

        token_pair = current_app.jwt_manager.create_token_pair(user.id)
        return jsonify({
            "message": "Login successful!",
            'token': token_pair.access_token,
            'refresh_token': token_pair.refresh_token
        }), 200

    def delete_all(self):
        result = self.auth_service.delete_all_users()
        if result:
            return jsonify({
                "message": "Tous les utilisateurs ont été supprimés."}), 200
        return jsonify({
            "error": "Erreur lors de la suppression des utilisateurs"}), 500
