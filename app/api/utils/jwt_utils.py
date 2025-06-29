import os
import jwt
from datetime import datetime, timezone
from flask import request, jsonify, current_app
from functools import wraps

SECRET = os.getenv("FLASK_SECRET_KEY")
ALGORITHM = "HS256"

# Verifying the token and extracting its payload
def decode_token(token):
    return jwt.decode(token, SECRET, algorithms=[ALGORITHM])

# Decorator for protected routes
def jwt_required(fn):
    @wraps(fn)
    def wrapper(*args, **kwargs):
        auth_header = request.headers.get("Authorization", "")
        if not auth_header.startswith("Bearer "):
            return jsonify({"error": "Authorization header missing or invalid"}), 401

        token = auth_header.split(" ", 1)[1]
        try:
            payload = decode_token(token)
            # Optional extra check: expiration
            exp = payload.get("exp")
            if exp and datetime.now(timezone.utc).timestamp() > exp:
                return jsonify({"error": "Token expired"}), 401
            # Attach user_id to Flask global if needed
            request.user_id = payload.get("user_id")
        except jwt.PyJWTError:
            return jsonify({"error": "Invalid or expired token"}), 401

        return fn(*args, **kwargs)
    return wrapper
