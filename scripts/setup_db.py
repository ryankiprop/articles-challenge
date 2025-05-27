from lib.db.connection import get_connection

def run_schema():
    conn = get_connection()
    cursor = conn.cursor()
    with open("lib/db/schema.sql", "r") as f:
        cursor.executescript(f.read())
    conn.commit()
    conn.close()

if __name__ == "__main__":
    run_schema()
    print("Database schema setup completed.")
