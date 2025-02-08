# app/api/routes/auth_routes.py
from flask import Blueprint
from app.api.controllers import AuthController
from app.utils.decorator import exception_handler

auth_bp = Blueprint('auth', __name__)
auth_controller = AuthController()

@auth_bp.route('/register', methods=['POST'])
@exception_handler
def register():
    return auth_controller.register()

@auth_bp.route('/login', methods=['POST'])
@exception_handler
def login():
    return auth_controller.login()

@auth_bp.route('/delete', methods=['DELETE'])
@exception_handler
def delete_all():
    return auth_controller.delete_all()
