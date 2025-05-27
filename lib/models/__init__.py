from lib.db.connection import get_connection

class BaseModel:
    @classmethod
    def _execute_query(cls, query, params=(), fetch_one=False, fetch_all=False, commit=False):
       """Helper method to execute database queries"""
       conn = get_connection()
       cursor = conn.cursor()
       try:
        # Ensure we're only executing one statement
           if ';' in query:
              raise ValueError("Multiple statements not allowed in single execute()")
            
            cursor.execute(query, params)
            if commit:
                conn.commit()
            if fetch_one:
                return cursor.fetchone()
            if fetch_all:
                return cursor.fetchall()
            return cursor
        except Exception as e:
            conn.rollback()
            raise e
        finally:
            conn.close()
    

    @classmethod
    def create_table(cls):
        """Create the table if it doesn't exist"""
        with open('lib/db/schema.sql') as f:
            schema = f.read()
        cls._execute_query(schema, commit=True)

    @classmethod
    def drop_table(cls):
        """Drop the table (for testing)"""
        cls._execute_query(f"DROP TABLE IF EXISTS {cls.TABLE_NAME}", commit=True)