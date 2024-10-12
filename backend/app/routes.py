from flask import jsonify, Blueprint, request
from app.models import db, User, bcrypt
# Pas besoin de créer une nouvelle instance ici
# app = create_app()  # Cette ligne est à retirer
bp = Blueprint("api", __name__)

@bp.route('/')
def home():
    print("coucou")
    return jsonify({'message': 'Hello from Fiesta de los Muertos!'})

@bp.route('/submit', methods=['POST'])
def submit_word():
    data = request.get_json()
    word = data.get('word')
    # Logique pour traiter le mot, par exemple, ajouter à une liste ou valider
    return jsonify(message=f"Mot '{word}' reçu!")


auth_bp = Blueprint('auth', __name__)

@auth_bp.route('/register', methods=['POST'])
def register():
    data = request.get_json()
    username = data.get('username')
    password = data.get('password')

    # Vérification des données
    if not username or not password:
        return jsonify({"message": "Username and password are required."}), 400

    # Vérifier si l'utilisateur existe déjà
    existing_user = User.query.filter_by(username=username).first()
    if existing_user:
        return jsonify({"message": "User already exists."}), 400

    # Hacher le mot de passe et créer un nouvel utilisateur
    hashed_password = bcrypt.generate_password_hash(password).decode('utf-8')
    new_user = User(username=username, password=hashed_password)
    db.session.add(new_user)
    db.session.commit()

    return jsonify({"message": "User created successfully."}), 201

