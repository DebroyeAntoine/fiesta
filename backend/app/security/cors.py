# security/cors.py
from flask_cors import CORS
from app.config.config import AppConfig

def setup_cors(app, config: AppConfig):
    CORS(app,
         resources={
             r"/*": {
                 "origins": config.security.allowed_origins,
                 "methods": ["GET", "POST", "PUT", "DELETE", "OPTIONS"],
                 "allow_headers": ["Content-Type", "Authorization"],
                 "expose_headers": ["Content-Range", "X-Content-Range"]
             }
         })
