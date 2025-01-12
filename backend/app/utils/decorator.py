from functools import wraps
from flask import jsonify, g, request, current_app
from jwt.exceptions import ExpiredSignatureError, InvalidTokenError

def exception_handler(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except Exception as e: # pylint: disable=broad-exception-caught
            print(f"Error in {func.__name__}: {e}")
            return jsonify({"error": "An internal error occurred",
                            "details": str(e)}), 500
    return wrapper

def jwt_required():
    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            auth_header = request.headers.get('Authorization')
            print(auth_header)
            if not auth_header or not auth_header.startswith('Bearer '):
                return jsonify({"error": "Missing or invalid token"}), 401

            token = auth_header.split(' ')[1]
            try:
                payload = current_app.jwt_manager.verify_token(token)
                g.jwt_identity = payload['sub']
                return f(*args, **kwargs)
            except ExpiredSignatureError:
                return jsonify({"error": "Token has expired"}), 401
            except InvalidTokenError:
                return jsonify({"error": "Invalid token"}), 401
        return decorated_function
    return decorator
