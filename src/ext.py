from flask_login import LoginManager
from flask_sqlalchemy import SQLAlchemy
from flask_socketio import SocketIO


login_manager = LoginManager()
db = SQLAlchemy()
socketio = SocketIO(cors_allowed_origins='*')