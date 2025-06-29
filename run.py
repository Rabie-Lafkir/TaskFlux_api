from flask import Flask
from dotenv import load_dotenv
import os
from app.api.utils.error_handlers import register_error_handlers
from app.db import close_pool

# Loading environment variables from .env
load_dotenv()

# Creating Flask app
app = Flask(__name__)
register_error_handlers(app)

#  Setting up secret key
app.config["SECRET_KEY"] = os.getenv("FLASK_SECRET_KEY")


# Importing and registering application routes
from app.api.routes.user_routes import user_bp
app.register_blueprint(user_bp, url_prefix="/api")

from app.api.routes.project_routes import project_bp
app.register_blueprint(project_bp, url_prefix="/api")

from app.api.routes.task_routes import task_bp
app.register_blueprint(task_bp, url_prefix="/api")


# Handling graceful shutdown
# @app.teardown_appcontext
# def shutdown_session(exception=None):
#     close_pool()


@app.route("/")
def index():
    return {"message":"Wecome to TaskFlux!!"}

# Launching app
if __name__ == "__main__":
    app.run(debug=True)