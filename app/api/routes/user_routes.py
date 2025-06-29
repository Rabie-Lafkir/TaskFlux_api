from flask import Blueprint, request, jsonify
from app.api.services import user_service
import jwt
import os
from datetime import datetime, timedelta,timezone

# Initializing blueprint
user_bp = Blueprint("user_bp", __name__)

# Getting secret key from .env
JWT_SECRET = os.getenv("FLASK_SECRET_KEY")
JWT_EXPIRATION_MINUTES = 30

# Registering new user
@user_bp.route("/users/register", methods=["POST"])
def register():
    data = request.get_json()
    required_fields = ["username", "email", "password"]
    if not all(field in data for field in required_fields):
        return jsonify({"error": "Missing required fields"}), 400

    user, error = user_service.register_user(
        username=data["username"],
        email=data["email"],
        password=data["password"],
        first_name=data.get("first_name"),
        last_name=data.get("last_name"),
        profile_pic=data.get("profile_pic")
    )

    if error:
        return jsonify({"error": error}), 400

    return jsonify({"message": "User registered successfully", "user": user}), 201


# Login
@user_bp.route("/users/login", methods=["POST"])
def login():
    data = request.get_json()
    if not data or not data.get("email") or not data.get("password"):
        return jsonify({"error": "Email and password required"}), 400

    user = user_service.authenticate_user(data["email"], data["password"])
    if not user:
        return jsonify({"error": "Invalid credentials"}), 401

    token = jwt.encode(
    {
        "user_id": user[0],
        "exp": datetime.now(timezone.utc) + timedelta(minutes=JWT_EXPIRATION_MINUTES)
    },
    JWT_SECRET,
    algorithm="HS256"
    )


    return jsonify({"token": token}), 200


# Getting user by ID
@user_bp.route("/users/<int:user_id>", methods=["GET"])
def get_user(user_id):
    user = user_service.get_user(user_id)
    if not user:
        return jsonify({"error": "User not found"}), 404
    return jsonify({"user": user}), 200


# Updating user
@user_bp.route("/users/<int:user_id>", methods=["PUT"])
def update_user(user_id):
    data = request.get_json()
    updated_user = user_service.update_user(
        user_id=user_id,
        username=data.get("username"),
        email=data.get("email"),
        first_name=data.get("first_name"),
        last_name=data.get("last_name"),
        profile_pic=data.get("profile_pic")
    )
    if not updated_user:
        return jsonify({"error": "User not found or update failed"}), 400
    return jsonify({"message": "User updated", "user": updated_user}), 200


# Deleting user
@user_bp.route("/users/<int:user_id>", methods=["DELETE"])
def delete_user(user_id):
    success = user_service.delete_user(user_id)
    if not success:
        return jsonify({"error": "User not found or could not be deleted"}), 400
    return jsonify({"message": "User deleted successfully"}), 200
