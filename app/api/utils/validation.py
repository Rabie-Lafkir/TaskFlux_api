"""
Simple request-body validation decorator for Flask + Pydantic.
Usage:

    from app.api.utils.validation import validate
    from app.api.schemas.user_schemas import UserRegisterSchema

    @bp.route("/users/register", methods=["POST"])
    @validate(UserRegisterSchema)
    def register():
        data = request.validated       # pydantic object
        ...
"""

from functools import wraps
from typing import Type

from flask import request, jsonify
from pydantic import BaseModel, ValidationError


def validate(schema: Type[BaseModel]):
    """
    Decorator that:
      • Reads and parses JSON from the request body.
      • Validates it with the given Pydantic schema.
      • On success – attaches the validated object to `request.validated`
        and calls the original view.
      • On failure – returns HTTP 422 with error details.
    """

    def decorator(fn):
        @wraps(fn)
        def wrapper(*args, **kwargs):
            try:
                payload = request.get_json(force=True, silent=False)
                obj = schema(**payload)
                # Expose to downstream code
                request.validated = obj
            except (TypeError, ValidationError) as err:
                # TypeError if payload is None or not JSON
                if isinstance(err, ValidationError):
                    error_response = {"errors": err.errors()}
                else:
                    error_response = {"errors": ["Request body must be valid JSON"]}
                return jsonify(error_response), 422

            return fn(*args, **kwargs)

        return wrapper

    return decorator
