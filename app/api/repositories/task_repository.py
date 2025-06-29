from app.db import get_db_connection, release_db_connection

# Creating a task
def create_task(title, project_id, description=None, due_date=None, status="pending", priority="medium", completed_at=None):
    conn = get_db_connection()
    if not conn:
        return None
    try:
        with conn.cursor() as cur:
            cur.execute("""
                INSERT INTO tasks (title, description, due_date, status, priority, completed_at, project_id)
                VALUES (%s, %s, %s, %s, %s, %s, %s)
                RETURNING id, title, description, due_date, status, priority, completed_at, project_id, created_at
            """, (title, description, due_date, status, priority, completed_at, project_id))
            task = cur.fetchone()
            conn.commit()
            return task
    except Exception as e:
        print("Error creating task:", e)
        conn.rollback()
        return None
    finally:
        release_db_connection(conn)

# Getting a task by ID
def get_task_by_id(task_id):
    conn = get_db_connection()
    if not conn:
        return None
    try:
        with conn.cursor() as cur:
            cur.execute("""
                SELECT id, title, description, due_date, status, priority, completed_at, project_id, created_at
                FROM tasks
                WHERE id = %s
            """, (task_id,))
            task = cur.fetchone()
            return task
    except Exception as e:
        print("Error fetching task by ID:", e)
        return None
    finally:
        release_db_connection(conn)

# Getting all tasks by project
def get_tasks_by_project(project_id):
    conn = get_db_connection()
    if not conn:
        return []
    try:
        with conn.cursor() as cur:
            cur.execute("""
                SELECT id, title, description, due_date, status, priority, completed_at, project_id, created_at
                FROM tasks
                WHERE project_id = %s
            """, (project_id,))
            tasks = cur.fetchall()
            return tasks
    except Exception as e:
        print("Error fetching tasks by project:", e)
        return []
    finally:
        release_db_connection(conn)

# Updating a task
def update_task(task_id, title=None, description=None, due_date=None, status=None, priority=None, completed_at=None):
    conn = get_db_connection()
    if not conn:
        return None
    try:
        with conn.cursor() as cur:
            cur.execute("""
                UPDATE tasks
                SET
                    title = COALESCE(%s, title),
                    description = COALESCE(%s, description),
                    due_date = COALESCE(%s, due_date),
                    status = COALESCE(%s, status),
                    priority = COALESCE(%s, priority),
                    completed_at = COALESCE(%s, completed_at)
                WHERE id = %s
                RETURNING id, title, description, due_date, status, priority, completed_at, project_id, created_at
            """, (title, description, due_date, status, priority, completed_at, task_id))
            updated_task = cur.fetchone()
            conn.commit()
            return updated_task
    except Exception as e:
        print("Error updating task:", e)
        conn.rollback()
        return None
    finally:
        release_db_connection(conn)

# Deleting a task
def delete_task(task_id):
    conn = get_db_connection()
    if not conn:
        return False
    try:
        with conn.cursor() as cur:
            cur.execute("DELETE FROM tasks WHERE id = %s", (task_id,))
            conn.commit()
            return cur.rowcount > 0
    except Exception as e:
        print("Error deleting task:", e)
        conn.rollback()
        return False
    finally:
        release_db_connection(conn)
