import app
from flask import request
from app import db, ma
from .models import User, user_schema, users_schema
#
#
# # Create a new user
# @app.route('/user', methods=['POST'])
# def create_user():
#     username = request.json['username']
#     email = request.json['email']
#     password = request.json['password']
#
#     new_user = User(username=username, email=email, password=password)
#
#     db.session.add(new_user)
#     db.session.commit()
#
#     return user_schema.jsonify(new_user)
#
#
# # Get all users
# @app.route('/user', methods=['GET'])
# def get_all_users():
#     all_users = User.query.all()
#     result = users_schema.dump(all_users)
#
#     return jsonify(result.data)
#
#
# # Get a single user
# @app.route('/user/<id>', methods=['GET'])
# def get_user(id):
#     user = User.query.get(id)
#     return user_schema.jsonify(user)
#
#
# # Update a user based on given id
# @app.route('/user/<id>', methods=['PUT'])
# def update_user(id):
#     user = User.query.get(id)
#
#     user.username = request.json['username']
#     user.email = request.json['email']
#     user.password = request.json['password']
#
#     db.session.commit()
#
#     return user_schema.jsonify(user)
#
#
# # Delete a user based on given id
# @app.route('/user/<id>', methods=['DELETE'])
# def delete_product(id):
#     user = User.query.get(id)
#
#     db.session.delete(user)
#     db.session.commit()
#
#     return user_schema.jsonify(user)
