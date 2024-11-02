from flask import Flask

from ext import socketio, db, login_manager
from router import apps
from soc import handle_connect, handle_send_private_message_event


def create_app():
    app = Flask(__name__)
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'
    app.config['SECRET_KEY'] = 'secret!'
    app.register_blueprint(apps)

    db.init_app(app)
    login_manager.init_app(app)
    socketio.init_app(app)
    login_manager.login_view = 'app_blueprint.login'

    with app.app_context():
        db.create_all()

    socketio.on_event('connect', handle_connect)
    socketio.on_event('send_private_message', handle_send_private_message_event)

    return app

if __name__ == '__main__':
    app=create_app()
    socketio.run(app,  debug=True, allow_unsafe_werkzeug=True)
