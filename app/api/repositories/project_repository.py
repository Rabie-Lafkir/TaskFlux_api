from app.db import get_db_connection, release_db_connection

# Create project
def create_project(name, user_id, description=None, start_date=None, end_date=None, status="active"):
    conn = get_db_connection()
    if not conn:
        return None
    try:
        with conn.cursor() as cur:
            cur.execute("""
                INSERT INTO projects (name, description, user_id, start_date, end_date, status)
                VALUES (%s, %s, %s, %s, %s, %s)
                RETURNING id, name, description, user_id, start_date, end_date, status, created_at
            """, (name, description, user_id, start_date, end_date, status))
            project = cur.fetchone()
            conn.commit()
            return project
    except Exception as e:
        print("Error creating project:", e)
        conn.rollback()
        return None
    finally:
        release_db_connection(conn)

# Get project by ID
def get_project_by_id(project_id):
    conn = get_db_connection()
    if not conn:
        return None
    try:
        with conn.cursor() as cur:
            cur.execute("""
                SELECT id, name, description, user_id, start_date, end_date, status, created_at
                FROM projects
                WHERE id = %s
            """, (project_id,))
            project = cur.fetchone()
            return project
    except Exception as e:
        print("Error fetching project by ID:", e)
        return None
    finally:
        release_db_connection(conn)

# Get projects by user
def get_projects_by_user(user_id):
    conn = get_db_connection()
    if not conn:
        return []
    try:
        with conn.cursor() as cur:
            cur.execute("""
                SELECT id, name, description, user_id, start_date, end_date, status, created_at
                FROM projects
                WHERE user_id = %s
            """, (user_id,))
            projects = cur.fetchall()
            return projects
    except Exception as e:
        print("Error fetching projects by user:", e)
        return []
    finally:
        release_db_connection(conn)

# Update project
def update_project(project_id, name=None, description=None, start_date=None, end_date=None, status=None):
    conn = get_db_connection()
    if not conn:
        return None
    try:
        with conn.cursor() as cur:
            cur.execute("""
                UPDATE projects
                SET
                    name = COALESCE(%s, name),
                    description = COALESCE(%s, description),
                    start_date = COALESCE(%s, start_date),
                    end_date = COALESCE(%s, end_date),
                    status = COALESCE(%s, status)
                WHERE id = %s
                RETURNING id, name, description, user_id, start_date, end_date, status, created_at
            """, (name, description, start_date, end_date, status, project_id))
            updated_project = cur.fetchone()
            conn.commit()
            return updated_project
    except Exception as e:
        print("Error updating project:", e)
        conn.rollback()
        return None
    finally:
        release_db_connection(conn)

# Delete project
def delete_project(project_id):
    conn = get_db_connection()
    if not conn:
        return False
    try:
        with conn.cursor() as cur:
            cur.execute("DELETE FROM projects WHERE id = %s", (project_id,))
            conn.commit()
            return cur.rowcount > 0
    except Exception as e:
        print("Error deleting project:", e)
        conn.rollback()
        return False
    finally:
        release_db_connection(conn)
