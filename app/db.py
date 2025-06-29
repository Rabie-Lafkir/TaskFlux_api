import os
from psycopg2 import pool
from dotenv import load_dotenv

# Loading environment variables from .env
load_dotenv()

DB_HOST = os.getenv("DB_HOST")
DB_NAME = os.getenv("DB_NAME")
DB_USER = os.getenv("DB_USER")
DB_PASSWORD = os.getenv("DB_PASSWORD")
DB_PORT = os.getenv("DB_PORT", 5432)

# Iniializing a connection pool 
try:
    connection_pool = pool.SimpleConnectionPool(
        minconn=1,
        maxconn=10,
        user=DB_USER,
        password=DB_PASSWORD,
        host=DB_HOST,
        port=DB_PORT,
        database=DB_NAME
    )
    if connection_pool:
        print("Connection pool created successfully")
except Exception as e:
    print("Error creating connection pool:", e)
    connection_pool = None

# Get a connection from the pool
def get_db_connection():
    try:
        conn = connection_pool.getconn()
        return conn
    except Exception as e:
        print("Error getting DB connection from pool", e)
        return None

# Return the connection to the pool
def release_db_connection(conn):
    if conn:
        connection_pool.putconn(conn)

#close the entire pool (typically on app shutdown)
def close_pool():
    """
    Closes all connections in the pool.
    """
    if connection_pool:
        connection_pool.closeall()
        print("Connection pool closed.")