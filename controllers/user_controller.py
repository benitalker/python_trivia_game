from dataclasses import asdict
from flask import Blueprint, jsonify, request
from model.User import User
from repository.user_repository import (
    get_all_users,
    find_user_by_id,
    create_user,
    update_user,
    delete_user
)

user_blueprint = Blueprint("users", __name__)

@user_blueprint.route("/users", methods=['GET'])
def get_all_users_route():
    users = list(map(asdict, get_all_users()))
    return jsonify(users), 200

@user_blueprint.route("/users/<int:user_id>", methods=['GET'])
def get_user_by_id(user_id):
    user = find_user_by_id(user_id)
    if user:
        return jsonify(asdict(user)), 200
    return jsonify({"error": "User not found"}), 404

@user_blueprint.route("/users", methods=['POST'])
def create_user_route():
    user_data = request.json
    new_user = User(**user_data)
    try:
        user_id = create_user(new_user)
        return jsonify({"id": user_id, "message": "User created successfully"}), 201
    except ValueError as e:
        return jsonify({"error": str(e)}), 400

@user_blueprint.route("/users/<int:user_id>", methods=['PUT'])
def update_user_route(user_id):
    user_data = request.json
    updated_user = User(**user_data)
    if update_user(user_id, updated_user):
        return jsonify({"message": "User updated successfully"}), 200
    return jsonify({"error": "User not found"}), 404

@user_blueprint.route("/users/<int:user_id>", methods=['DELETE'])
def delete_user_route(user_id):
    if delete_user(user_id):
        return jsonify({"message": "User deleted successfully"}), 200
    return jsonify({"error": "User not found"}), 404
