from flask import Flask, request, jsonify
from flask_login import UserMixin
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
from flask_jwt_extended import JWTManager, jwt_required, create_access_token

import os

# App Config
app = Flask(__name__)
basedir = os.path.abspath(os.path.dirname(__file__))

# Database Config
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'db.sqlite')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False


# Setup the Flask-JWT-Extended extension
app.config['JWT_SECRET_KEY'] = 'hol1Wda91239'
jwt = JWTManager(app)


@app.route('/login', methods=['POST'])
def login():
    if not request.is_json:
        return jsonify({"msg": "Missing JSON in request"}), 400

    username = request.json.get('username', None)
    password = request.json.get('password', None)
    if not username:
        return jsonify({"msg": "Missing username"}), 400
    if not password:
        return jsonify({"msg": "Missing password"}), 400

    user = User.query.filter_by(username=username, password=password)

    if user is None:
        return jsonify({"msg": "Wrong authentication credentials entered!"}), 401

    # Identity can be any data that is json serializable
    access_token = create_access_token(identity=username)
    return jsonify(access_token=access_token), 200


# Initialize DB
db = SQLAlchemy(app)

# Initialize MM
ma = Marshmallow(app)


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


# Create a new user
@app.route('/user', methods=['POST'])
def create_user():
    username = request.json['username']
    email = request.json['email']
    password = request.json['password']

    new_user = User(username=username, email=email, password=password)

    db.session.add(new_user)
    db.session.commit()

    return user_schema.jsonify(new_user)


# Get all users
@app.route('/user', methods=['GET'])
# Protect the view with jwt_required, which requires a valid access token in the request to access.
@jwt_required
def get_all_users():
    all_users = User.query.all()
    result = users_schema.dump(all_users)

    return jsonify(result.data)


# Get a single user
@app.route('/user/<id>', methods=['GET'])
# Protect the view with jwt_required, which requires a valid access token in the request to access.
@jwt_required
def get_user(id):
    user = User.query.get(id)
    return user_schema.jsonify(user)


# Update a user based on given id
@app.route('/user/<id>', methods=['PUT'])
# Protect the view with jwt_required, which requires a valid access token in the request to access.
@jwt_required
def update_user(id):
    user = User.query.get(id)

    user.username = request.json['username']
    user.email = request.json['email']
    user.password = request.json['password']

    db.session.commit()

    return user_schema.jsonify(user)


# Delete a user based on given id
@app.route('/user/<id>', methods=['DELETE'])
# Protect the view with jwt_required, which requires a valid access token in the request to access.
@jwt_required
def delete_user(id):
    user = User.query.get(id)

    db.session.delete(user)
    db.session.commit()

    return user_schema.jsonify(user)


@app.route("/hello")
def hello():
    return "Hello World!"


if __name__ == "__main__":
    app.run(debug=True)

