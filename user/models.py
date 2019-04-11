from app import db, ma
from flask_login import UserMixin


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(40), unique=True)
    email = db.Column(db.String(40), unique=True)
    password = db.Column(db.String(40))

    def __init__(self, username, email, password):
        self.username = username
        self.email = email
        self.password = password


# User Schema
class UserSchema(ma.Schema):
    class Meta:
        fields = ('id', 'username', 'email', 'password')


# Init Schema
user_schema = UserSchema(strict=True)
users_schema = UserSchema(many=True, strict=True)