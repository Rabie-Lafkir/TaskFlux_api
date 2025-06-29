from app.api.repositories import project_repository

# Creating a project
def create_project(name, user_id, description=None, start_date=None, end_date=None, status="active"):
    if not name or not user_id:
        return None, "Project name and user ID are required"
    
    project = project_repository.create_project(
        name=name,
        user_id=user_id,
        description=description,
        start_date=start_date,
        end_date=end_date,
        status=status
    )
    if project:
        return project, None
    else:
        return None, "Failed to create project"

# Getting a single project by ID
def get_project_by_id(project_id):
    return project_repository.get_project_by_id(project_id)

# Listing all projects for a user
def get_projects_by_user(user_id):
    return project_repository.get_projects_by_user(user_id)

# Updating a project
def update_project(project_id, name=None, description=None, start_date=None, end_date=None, status=None):
    updated_project = project_repository.update_project(
        project_id=project_id,
        name=name,
        description=description,
        start_date=start_date,
        end_date=end_date,
        status=status
    )
    if updated_project:
        return updated_project, None
    else:
        return None, "Project not found or update failed"

# Deleting a project
def delete_project(project_id):
    success = project_repository.delete_project(project_id)
    if success:
        return True, None
    else:
        return False, "Project not found or could not be deleted"
