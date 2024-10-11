from flask import Flask
from flask_cors import CORS

def create_app():
    app = Flask(__name__)
    CORS(app)
    from .routes import bp  # Importer les routes
    app.register_blueprint(bp)
    return app

