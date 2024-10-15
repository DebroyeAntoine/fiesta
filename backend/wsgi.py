from app import create_app
import datetime
from flask_jwt_extended import JWTManager, create_access_token, jwt_required, get_jwt_identity


app = create_app()

app.config['JWT_SECRET_KEY'] = 'your_jwt_secret_key_here'
app.config['JWT_ACCESS_TOKEN_EXPIRES'] = datetime.timedelta(minutes=15)
jwt = JWTManager(app)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
