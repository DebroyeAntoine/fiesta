from functools import wraps
from flask import jsonify, g, request, current_app

def exception_handler(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except Exception as e:
            print(f"Error in {func.__name__}: {e}")  # Log the error for debugging
            return jsonify({"error": "An internal error occurred", "details": str(e)}), 500
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
            except Exception as e:
                return jsonify({"error": str(e)}), 401
        return decorated_function
    return decorator

def get_jwt_identity():
    return g.jwt_identity if hasattr(g, 'jwt_identity') else None


