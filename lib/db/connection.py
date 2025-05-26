import sqlite3
from sqlite3 import Error

def get_connection():
    """Create a database connection to a SQLite database"""
    conn = None
    try:
        conn = sqlite3.connect('articles.db')
        conn.row_factory = sqlite3.Row
        return conn
    except Error as e:
        print(f"Error connecting to database: {e}")
        raise

def setup_database():
    """Initialize the database with schema"""
    conn = get_connection()
    try:
        with open('lib/db/schema.sql', 'r') as f:
            conn.executescript(f.read())
        conn.commit()
    except Error as e:
        print(f"Error setting up database: {e}")
        raise
    finally:
        if conn:
            conn.close()