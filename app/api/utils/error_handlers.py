from flask import jsonify
from werkzeug.exceptions import HTTPException

def register_error_handlers(app):
    # Handle any Werkzeug-derived HTTPException (e.g., 404, 400)
    @app.errorhandler(HTTPException)
    def handle_http_error(err):
        response = {
            "error": {
                "type": err.__class__.__name__,   # e.g. NotFound, BadRequest
                "message": err.description or "Unexpected error"
            }
        }
        return jsonify(response), err.code

    # Catch everything else → 500
    @app.errorhandler(Exception)
    def handle_generic_error(err):
        # You can log the traceback here if wanted
        response = {
            "error": {
                "type": "InternalServerError",
                "message": "An unexpected error occurred"
            }
        }
        return jsonify(response), 500
