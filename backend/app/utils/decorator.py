from functools import wraps
from flask import jsonify

def exception_handler(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except Exception as e:
            print(f"Error in {func.__name__}: {e}")  # Log the error for debugging
            return jsonify({"error": "An internal error occurred", "details": str(e)}), 500
    return wrapper

