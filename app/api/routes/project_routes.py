from flask import Blueprint, request, jsonify
from app.api.schemas.project_schemas import ProjectCreateSchema
from app.api.services import project_service
from app.api.utils.jwt_utils import jwt_required
from app.api.utils.validation import validate

project_bp = Blueprint("project_bp", __name__)

# Creating a project
@project_bp.route("/projects", methods=["POST"])
@jwt_required
@validate(ProjectCreateSchema)
def create_project():
    data = request.get_json()
    required_fields = ["name", "user_id"]
    if not all(field in data for field in required_fields):
        return jsonify({"error": "name and user_id are required"}), 400
    
    project, error = project_service.create_project(
        name=data["name"],
        user_id=data["user_id"],
        description=data.get("description"),
        start_date=data.get("start_date"),
        end_date=data.get("end_date"),
        status=data.get("status", "active")
    )
    if error:
        return jsonify({"error": error}), 400
    
    return jsonify({"message": "Project created successfully", "project": project}), 201

# Getting all projects for a user
@project_bp.route("/projects/user/<int:user_id>", methods=["GET"])
@jwt_required
def get_projects_by_user(user_id):
    projects = project_service.get_projects_by_user(user_id)
    return jsonify({"projects": projects}), 200

# Getting a project by ID
@project_bp.route("/projects/<int:project_id>", methods=["GET"])
@jwt_required
def get_project(project_id):
    project = project_service.get_project_by_id(project_id)
    if not project:
        return jsonify({"error": "Project not found"}), 404
    return jsonify({"project": project}), 200

# Updating a project
@project_bp.route("/projects/<int:project_id>", methods=["PUT"])
@jwt_required
@validate(ProjectCreateSchema)
def update_project(project_id):
    data = request.get_json()
    project, error = project_service.update_project(
        project_id=project_id,
        name=data.get("name"),
        description=data.get("description"),
        start_date=data.get("start_date"),
        end_date=data.get("end_date"),
        status=data.get("status")
    )
    if error:
        return jsonify({"error": error}), 400
    return jsonify({"message": "Project updated", "project": project}), 200

# Deleting a project
@project_bp.route("/projects/<int:project_id>", methods=["DELETE"])
@jwt_required
def delete_project(project_id):
    success, error = project_service.delete_project(project_id)
    if not success:
        return jsonify({"error": error}), 400
    return jsonify({"message": "Project deleted successfully"}), 200
