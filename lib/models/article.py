from lib.db import get_connection

class Article:
    def __init__(self, id, title, content, author_id, magazine_id):
        self.id = id
        self.title = title
        self.content = content
        self.author_id = author_id
        self.magazine_id = magazine_id

    @classmethod
    def create(cls, title, author_id, magazine_id, content):
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute(
            "INSERT INTO articles (title, content, author_id, magazine_id) VALUES (?, ?, ?, ?)",
            (title, content, author_id, magazine_id)
        )
        conn.commit()
        article_id = cursor.lastrowid
        conn.close()
        return cls(article_id, title, content, author_id, magazine_id)

    @classmethod
    def find_by_id(cls, id):
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute(
            "SELECT id, title, content, author_id, magazine_id FROM articles WHERE id = ?", (id,)
        )
        row = cursor.fetchone()
        conn.close()
        if row:
            return cls(row[0], row[1], row[2], row[3], row[4])
        return None
