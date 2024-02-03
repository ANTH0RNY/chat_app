from . import api
from flask import request, jsonify
from app import jwt, db
from app.models import User, TokenBlocklist, Message
from flask_jwt_extended import create_access_token, current_user, jwt_required, get_jwt
from datetime import datetime, timezone
from sqlalchemy import or_, and_
from sqlalchemy.exc import IntegrityError

@jwt.user_identity_loader
def user_identity_lookup(user):
    return user.id


@jwt.user_lookup_loader
def user_lookup_callback(jwt_header, jwt_data):
    identity = jwt_data["sub"]
    return User.query.filter_by(id=identity).one_or_none()


@jwt.token_in_blocklist_loader
def check_if_token_revoked(jwt_header, jwt_payload: dict) -> bool:
    jti = jwt_payload["jti"]
    token = db.session.query(TokenBlocklist.id).filter_by(jti=jti).scalar()

    return token is not None


@api.route("/login", methods=["POST"])
def login():
    username = request.json.get("username", None)
    password = request.json.get("password", None)

    if username is None or password is None:
        return jsonify("Bad request"), 400
    user = User.query.filter_by(username=username).one_or_none()
    if not user or not user.verify_password(password):
        return jsonify(msg="Wrong username or password"), 401

    access_token = create_access_token(identity=user)
    return jsonify(msg="login succeful", access_token=access_token)


@api.route("/logout")
@jwt_required()
def modify_token():
    jti = get_jwt()["jti"]
    now = datetime.now(timezone.utc)
    db.session.add(TokenBlocklist(jti=jti, created_at=now))
    db.session.commit()
    return jsonify(msg="JWT revoked")


@api.route("/user", methods=["GET", "Post"])
@jwt_required(optional=True)
def user():
    print(current_user)
    if request.method == "GET":
        if current_user is None:
            return jsonify({'msg':'UNAUTHORIZED'}), 401
        return jsonify({'id': current_user.id, 'username': current_user.username})

    username = request.json.get("username", None)
    password = request.json.get("password", None)

    if username is None or password is None or password == "":
        return jsonify(msg="Bad request"), 400
    user = User.query.filter_by(username=username).one_or_none()
    if user is not None:
        return jsonify({"msg": "Wrong operation"}), 400
    new_user = User(username=username, password=password)
    db.session.add(new_user)
    db.session.commit()
    return jsonify({"msg":"User added successfully"}), 201


@api.route("/message/<int:id>", methods=["GET", "POST"])
@jwt_required()
def messages(id):
    if request.method == "GET":
        # user = User.query.filter_by(id=id).first()
        sender_id= current_user.id
        recipient_id = id
        messages  = Message.query.filter(or_(and_(Message.sender == sender_id, Message.recipient == recipient_id), and_(Message.sender == recipient_id, Message.recipient == sender_id))).order_by(Message.date_created.desc()).all()
        messages_object=[{'id': x.id, 'to': {"id": x.To.id, "username":x.To.username}, 'from': {"id":x.From.id, "username":x.From.username}, 'body': x.body, 'date_created': x.date_created} for x in messages]
        # print(len(messages_object))
        return jsonify(messages_object)
    if id == current_user.id:
        return jsonify({'msg': "Can't send message to yourself"}), 401
    body = request.json.get("body", None)
    recipient = User.query.filter_by(id=id).first()
    if body is None or recipient is None:
        return jsonify({'msg': "Bad request"}), 400
    new_message = Message(sender= current_user.id, recipient = recipient.id, body=body)
    db.session.add(new_message)
    try:
        db.session.commit()
    except IntegrityError:
        db.session.roll_back()
        return jsonify({'msg': "something went wrong contact administrator"}), 500

    return jsonify({'msg': 'Message added successfully'}), 201


# db.session.query(User).join(Message, db.or_(Message.sender == User.id, Message.recipient == User.id))
# .filter(db.or_(Message.sender == 2, Message.recipient== 2)).filter(User.id != 2).order_by(Message.date_created).all()

# User.query.join(Message, db.or_(Message.sender == User.id, Message.recipient == User.id))
# .filter(db.or_(Message.sender == 2, Message.recipient==2)).filter(User.id != 2).order_by(Message.date_created).all()
@api.route('/contacts')
@jwt_required()
def get_contacts():
    users = db.session.query(User).join(Message, db.or_(Message.sender == User.id, Message.recipient == User.id))\
            .filter(db.or_(Message.sender == current_user.id, Message.recipient== current_user.id)).filter(User.id != current_user.id).order_by(Message.date_created.desc()).all()
    contacts = [{"id":x.id, "username": x.username} for x in users]
    return jsonify(contacts)

@api.route("/add_message/<string:username>", methods=["POST"])
@jwt_required()
def add_message_by_username(username):
    user = User.query.filter_by(username = username).first()
    body = request.json.get("body", None)
    if user is None or body is None:
        return jsonify({"msg": "bad request"}), 400
    
    message = Message(sender=current_user.id, recipient=user.id, body=body)
    db.session.add(message)
    try:
        db.session.commit()
    except IntegrityError:
        db.session.roll_back()
        return jsonify(msg="Something went wrong contact admininistrator"), 500
    return jsonify({"msg": "Message added successfully"}), 201

@api.route("/")
def index():
    return jsonify({"msg":"hello"})
