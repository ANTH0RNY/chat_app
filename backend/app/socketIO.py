from sqlalchemy import event
from sqlalchemy.exc import IntegrityError
from . import socketio
from flask_socketio import emit, ConnectionRefusedError, join_room
from flask_jwt_extended import decode_token
from .models import User, Message
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
        emit("echo", "you have been connected")
        return jwt_data[0]
    except (KeyError, json.decoder.JSONDecodeError):
        raise ConnectionRefusedError("token not given or auth is in wrong format")


@event.listens_for(Message, "after_insert")
def send_message(mapper, connection, instance):
    recipient = User.query.filter_by(id=instance.recipient).first()
    sender = User.query.filter_by(id=instance.sender).first()

    if sender is None or recipient is None:
        raise IntegrityError(
            "Message has invalid recipient or sender, the recipient or sender is not in User table"
        )

    message_object = {
        "id": instance.id,
        "to": {
            "id": recipient.id,
            "username": recipient.username,
        },
        "from":{
            "id": sender.id,
            "username": sender.username
        },
        "body": instance.body,
        "date_created": instance.date_created.isoformat(),
    }
    socketio.emit(recipient.username, message_object)
