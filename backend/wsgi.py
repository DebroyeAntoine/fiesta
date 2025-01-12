import datetime
from app import create_app
from flask_jwt_extended import JWTManager
from app.socket import socketio

app = create_app()

# Initialize SocketIO with app
socketio.init_app(app, async_mode='eventlet')

if __name__ == '__main__':
    socketio.run(app, host='0.0.0.0', port=5000, debug=True)
