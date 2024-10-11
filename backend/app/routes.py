from flask import jsonify, Blueprint, request

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
