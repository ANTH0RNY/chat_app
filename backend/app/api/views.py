from . import api
from flask import request, jsonify
from app import jwt, db
from app.models import User, TokenBlocklist
from flask_jwt_extended import create_access_token, current_user, jwt_required, get_jwt
from datetime import datetime, timezone


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
        return jsonify("Wrong username or password"), 401

    access_token = create_access_token(identity=user)
    return jsonify(access_token=access_token)


@api.route("/logout")
@jwt_required()
def modify_token():
    jti = get_jwt()["jti"]
    now = datetime.now(timezone.utc)
    db.session.add(TokenBlocklist(jti=jti, created_at=now))
    db.session.commit()
    return jsonify(msg="JWT revoked")


@api.route("/users", methods=["GET", "Post"])
@jwt_required(optional=True)
def user():
    print(current_user)
    if request.method == "GET":
        if current_user is None:
            return jsonify({msg:'UNAUTHORIZED'}), 401
        return jsonify({'id': current_user.id, 'username': current_user.username})
        
    username = request.json.get("username", None)
    password = request.json.get("password", None)

    if username is None or password is None or password == "":
        return jsonify("Bad request"), 400
    user = User.query.filter_by(username=username).one_or_none()
    if user is not None:
        return jsonify("Wrong operation"), 405
    new_user = User(username=username, password=password)
    db.session.add(new_user)
    db.session.commit()
    return jsonify("User added successfully"), 201
