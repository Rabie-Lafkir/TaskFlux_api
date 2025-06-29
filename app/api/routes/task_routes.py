from flask import Blueprint, request, jsonify
from app.api.schemas.task_schemas import TaskCreateSchema
from app.api.services import task_service
from app.api.utils.jwt_utils import jwt_required
from app.api.utils.validation import validate

task_bp = Blueprint("task_bp", __name__)

# Creating a task
@task_bp.route("/tasks", methods=["POST"])
@jwt_required
@validate(TaskCreateSchema)
def create_task():
    data = request.get_json()
    required_fields = ["title", "project_id"]
    if not all(field in data for field in required_fields):
        return jsonify({"error": "title and project_id are required"}), 400
    
    task, error = task_service.create_task(
        title=data["title"],
        project_id=data["project_id"],
        description=data.get("description"),
        due_date=data.get("due_date"),
        status=data.get("status", "pending"),
        priority=data.get("priority", "medium"),
        completed_at=data.get("completed_at")
    )
    if error:
        return jsonify({"error": error}), 400
    
    return jsonify({"message": "Task created successfully", "task": task}), 201

# Getting a task by ID
@task_bp.route("/tasks/<int:task_id>", methods=["GET"])
@jwt_required
def get_task(task_id):
    task = task_service.get_task_by_id(task_id)
    if not task:
        return jsonify({"error": "Task not found"}), 404
    return jsonify({"task": task}), 200

# Getting all tasks by project
@task_bp.route("/tasks/project/<int:project_id>", methods=["GET"])
@jwt_required
def get_tasks_by_project(project_id):
    tasks = task_service.get_tasks_by_project(project_id)
    return jsonify({"tasks": tasks}), 200

# Updating a task
@task_bp.route("/tasks/<int:task_id>", methods=["PUT"])
@jwt_required
@validate(TaskCreateSchema)
def update_task(task_id):
    data = request.get_json()
    task, error = task_service.update_task(
        task_id=task_id,
        title=data.get("title"),
        description=data.get("description"),
        due_date=data.get("due_date"),
        status=data.get("status"),
        priority=data.get("priority"),
        completed_at=data.get("completed_at")
    )
    if error:
        return jsonify({"error": error}), 400
    return jsonify({"message": "Task updated successfully", "task": task}), 200

# Deleting a task
@task_bp.route("/tasks/<int:task_id>", methods=["DELETE"])
@jwt_required
def delete_task(task_id):
    success, error = task_service.delete_task(task_id)
    if not success:
        return jsonify({"error": error}), 400
    return jsonify({"message": "Task deleted successfully"}), 200
