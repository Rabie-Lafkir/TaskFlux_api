from app.api.repositories import task_repository

# Creating a task
def create_task(title, project_id, description=None, due_date=None, status="pending", priority="medium", completed_at=None):
    if not title or not project_id:
        return None, "Task title and project ID are required"
    
    task = task_repository.create_task(
        title=title,
        project_id=project_id,
        description=description,
        due_date=due_date,
        status=status,
        priority=priority,
        completed_at=completed_at
    )
    
    if task:
        return task, None
    else:
        return None, "Failed to create task"

# Getting a task by ID
def get_task_by_id(task_id):
    return task_repository.get_task_by_id(task_id)

# Getting all tasks by project
def get_tasks_by_project(project_id):
    return task_repository.get_tasks_by_project(project_id)

# Updating a task
def update_task(task_id, title=None, description=None, due_date=None, status=None, priority=None, completed_at=None):
    updated_task = task_repository.update_task(
        task_id=task_id,
        title=title,
        description=description,
        due_date=due_date,
        status=status,
        priority=priority,
        completed_at=completed_at
    )
    if updated_task:
        return updated_task, None
    else:
        return None, "Task not found or update failed"

# Deleting a task
def delete_task(task_id):
    success = task_repository.delete_task(task_id)
    if success:
        return True, None
    else:
        return False, "Task not found or could not be deleted"
