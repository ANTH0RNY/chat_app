from flask import Flask
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy
from flask_jwt_extended import JWTManager
from flask_socketio import SocketIO, emit
from config import config

db = SQLAlchemy()
migrate = Migrate()
jwt = JWTManager()
socketio = SocketIO()


def create_app(config_name="default"):
    app = Flask(__name__)
    app.config.from_object(config[config_name])

    db.init_app(app)
    jwt.init_app(app)
    migrate.init_app(app, db)
    socketio.init_app(app, cors_allowed_origins=["http://localhost:5173"])

    from .api import api

    app.register_blueprint(api)

    return app


from .socketIO import *
