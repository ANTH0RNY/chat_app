from . import db
from werkzeug.security import generate_password_hash, check_password_hash


class User(db.Model):
    __tablename__ = "User"
    id = db.Column(db.Integer(), primary_key=True)
    username = db.Column(db.String(64), unique=True, index=True)
    password_hash = db.Column(db.String(128))
    
    sender = db.relationship("Message", backref="From", foreign_keys="Message.sender")
    recipient = db.relationship(
        "Message", backref="To", foreign_keys="Message.recipient"
    )

    @property
    def password(hash):
        raise AttributeError("Password is not a readable attribute")

    @password.setter
    def password(self, password):
        self.password_hash = generate_password_hash(password)

    def verify_password(self, password):
        return check_password_hash(self.password_hash, password)


class Message(db.Model):
    __tablename__ = "Message"
    id = db.Column(db.Integer, primary_key=True)
    sender = db.Column(db.Integer, db.ForeignKey("User.id"))
    recipient = db.Column(db.Integer, db.ForeignKey("User.id"))
    body = db.Column(db.Text)
