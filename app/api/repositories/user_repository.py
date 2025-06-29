from app.db import get_db_connection, release_db_connection

# Creating user 
def create_user(username, email, password_hash, first_name=None, last_name=None, profile_pic=None):
    conn = get_db_connection()
    if not conn:
        return None
    try:
        with conn.cursor() as cur:
            cur.execute("""
                INSERT INTO users (username, email, password_hash, first_name, last_name, profile_pic)
                VALUES (%s, %s, %s, %s, %s, %s)
                RETURNING id, username, email, first_name, last_name, profile_pic, created_at
            """, (username, email, password_hash, first_name, last_name, profile_pic))
            user = cur.fetchone()
            conn.commit()
            return user
    except Exception as e:
        print("Error creating user:", e)
        conn.rollback()
        return None
    finally:
        release_db_connection(conn)

# Getting user by ID
def get_user_by_id(user_id):
    conn = get_db_connection()
    if not conn:
        return None
    try:
        with conn.cursor() as cur:
             cur.execute("""
                SELECT id, username, email, first_name, last_name, profile_pic, created_at
                FROM users
                WHERE id = %s
            """, (user_id,))
             user = cur.fetchone()
             return user
    except Exception as e:
        print("Error fetching user by ID:", e) 
        conn.rollback()
        return None
    finally:
        release_db_connection(conn)


# Getting user by email
def get_user_by_email(email):
    conn = get_db_connection()
    if not conn:
        return None
    try:
        with conn.cursor() as cur:
             cur.execute("""
                SELECT id, username, email, password_hash, first_name, last_name, profile_pic, created_at
                FROM users
                WHERE email = %s
            """, (email,))
             user = cur.fetchone()
             return user
    except Exception as e:
        print("Error fetching user by email:", e)
        return None
    finally:
        release_db_connection(conn)

# Updating user
def update_user(user_id, username=None, email=None, first_name=None, last_name=None, profile_pic=None):
    conn = get_db_connection()
    if not conn:
        return None
    try:
        with conn.cursor() as cur:
            cur.execute("""
                UPDATE users
                SET
                    username = COALESCE(%s, username),
                    email = COALESCE(%s, email),
                    first_name = COALESCE(%s, first_name),
                    last_name = COALESCE(%s, last_name),
                    profile_pic = COALESCE(%s, profile_pic)
                WHERE id = %s
                RETURNING id, username, email, first_name, last_name, profile_pic, created_at
            """, (username, email, first_name, last_name, profile_pic, user_id))
            updated_user = cur.fetchone()
            conn.commit()
            return updated_user
    except Exception as e:
        print("Error updating user", e)
        conn.rollback()
        return None
    finally:
        release_db_connection(conn)

# Deleting user
def delete_user(user_id):
    conn = get_db_connection()
    if not conn:
        return False
    try:
        with conn.cursor() as cur:
            cur.execute("DELETE FROM users WHERE id = %s", (user_id,))
            conn.commit()
            return cur.rowcount > 0  # returns True if something was deleted
    except Exception as e:
        print("Error deleting user:", e)
        conn.rollback()
        return False
    finally:
        release_db_connection(conn)