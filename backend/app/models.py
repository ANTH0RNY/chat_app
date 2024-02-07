from . import db, jwt
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime


class User(db.Model):
    __tablename__ = "User"
    id = db.Column(db.Integer(), primary_key=True)
    username = db.Column(db.String(64), unique=True, index=True)
    password_hash = db.Column(db.String(128))
    profile_url = db.Column(
        db.String(), default="https://picsum.photos/seed/picsum/200", nullable=False
    )
    last_seen = db.Column(db.DateTime, default=datetime.utcnow)

    sender = db.relationship(
        "Message", backref="From", foreign_keys="Message.sender", lazy="dynamic"
    )
    recipient = db.relationship(
        "Message", backref="To", foreign_keys="Message.recipient", lazy="dynamic"
    )

    @property
    def password(hash):
        raise AttributeError("Password is not a readable attribute")

    @password.setter
    def password(self, password):
        self.password_hash = generate_password_hash(password)

    def verify_password(self, password):
        return check_password_hash(self.password_hash, password)

    def ping(self):
        self.last_seen = datetime.utcnow()
        db.session.add(self)
        db.session.commit()


class Message(db.Model):
    __tablename__ = "Message"
    id = db.Column(db.Integer, primary_key=True)
    sender = db.Column(db.Integer, db.ForeignKey("User.id"), index=True)
    recipient = db.Column(db.Integer, db.ForeignKey("User.id"), index=True)
    body = db.Column(db.Text)
    date_created = db.Column(db.DateTime, default=datetime.utcnow)

    def __str__(self) -> str:
        return f"sender: {self.sender} recipient: {self.recipient} date: {self.date_created}"


class TokenBlocklist(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    jti = db.Column(db.String(36), nullable=False, index=True)
    created_at = db.Column(db.DateTime, nullable=False)
