from lib.db.connection import get_connection
from lib.models.author import Author
from lib.models.article import Article

def add_author_with_articles(author_name, articles_data):
    """
    Add an author and their articles in a single transaction
    articles_data: list of dicts with 'title' and 'magazine_id' keys
    """
    conn = get_connection()
    try:
        conn.execute("BEGIN")
        cursor = conn.cursor()
        
        # Insert author
        cursor.execute(
            "INSERT INTO authors (name) VALUES (?) RETURNING id",
            (author_name,)
        )
        author_id = cursor.fetchone()[0]
        
        # Insert articles
        for article in articles_data:
            cursor.execute(
                "INSERT INTO articles (title, author_id, magazine_id) VALUES (?, ?, ?)",
                (article['title'], author_id, article['magazine_id'])
            )
        
        conn.commit()
        return Author.find_by_id(author_id)
    except Exception as e:
        conn.rollback()
        raise e
    finally:
        conn.close()