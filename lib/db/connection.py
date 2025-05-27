import os
import sqlite3
from sqlite3 import Error

# lib/db/connection.py
import os
import sqlite3
from sqlite3 import Error

def get_connection():
    """Create a database connection"""
    if os.getenv('TESTING'):
        # Use in-memory database for tests
        conn = sqlite3.connect(':memory:')
    else:
        # Use file-based database for production
        conn = sqlite3.connect('articles.db')
    
    conn.row_factory = sqlite3.Row
    return conn

def setup_database():
    """Initialize the database with schema"""
    conn = get_connection()
    try:
        with open('lib/db/schema.sql', 'r') as f:
            sql_script = f.read()
        
        # Split the script into individual statements
        statements = [stmt.strip() for stmt in sql_script.split(';') if stmt.strip()]
        
        for statement in statements:
            conn.execute(statement)
        
        conn.commit()
    except Error as e:
        print(f"Error setting up database: {e}")
        raise
    finally:
        if conn:
            conn.close()