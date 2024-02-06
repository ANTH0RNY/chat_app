from . import socketio
from flask_socketio import emit, ConnectionRefusedError, join_room
from flask_jwt_extended import decode_token
from .models import User
import json


def validate_jwt(jwt_token):
    try:
        payload = decode_token(jwt_token)
        return True, payload
    except Exception as e:
        return False, str(e)


@socketio.on("connect")
def connect(auth):
    if auth is None:
        raise ConnectionRefusedError("Passed no auth object")
    try:
        token = json.loads(auth)
        jwt_data = validate_jwt(token["token"])
        if not jwt_data[0]:
            raise ConnectionRefusedError(jwt_data[1])
        user = User.query.filter_by(id=jwt_data[1]["sub"]).one_or_none()
        if user is None:
            raise ConnectionRefusedError("Something went wrong contact administrator")
        join_room(user.username)
        emit("connected", "you have been connected")
        return jwt_data[0]
    except (KeyError, json.decoder.JSONDecodeError):
        raise ConnectionRefusedError("token not given or auth is in wrong format")
