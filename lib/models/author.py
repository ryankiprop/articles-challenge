from lib.models import BaseModel
from lib.db.connection import get_connection

class Author(BaseModel):
    TABLE_NAME = "authors"

    def __init__(self, id=None, name=None):
        self.id = id
        self.name = name

    def save(self):
        """Save the author to the database"""
        if not self.name:
            raise ValueError("Author name cannot be empty")

        if self.id:
            query = "UPDATE authors SET name = ? WHERE id = ?"
            params = (self.name, self.id)
        else:
            query = "INSERT INTO authors (name) VALUES (?) RETURNING id"
            params = (self.name,)

        result = self._execute_query(query, params, fetch_one=True, commit=True)
        if not self.id:
            self.id = result[0]
        return self

    def delete(self):
        """Delete the author from the database"""
        if self.id:
            self._execute_query(
                "DELETE FROM authors WHERE id = ?",
                (self.id,),
                commit=True
            )

    @classmethod
    def find_by_id(cls, id):
        """Find an author by ID"""
        result = cls._execute_query(
            "SELECT * FROM authors WHERE id = ?",
            (id,),
            fetch_one=True
        )
        return cls(**result) if result else None

    @classmethod
    def find_by_name(cls, name):
        """Find authors by name"""
        results = cls._execute_query(
            "SELECT * FROM authors WHERE name = ?",
            (name,),
            fetch_all=True
        )
        return [cls(**row) for row in results]

    @classmethod
    def get_all(cls):
        """Get all authors"""
        results = cls._execute_query("SELECT * FROM authors", fetch_all=True)
        return [cls(**row) for row in results]

    def articles(self):
        """Get all articles written by this author"""
        from lib.models.article import Article
        results = self._execute_query(
            "SELECT * FROM articles WHERE author_id = ?",
            (self.id,),
            fetch_all=True
        )
        return [Article(**row) for row in results]

    def magazines(self):
        """Get all magazines this author has written for"""
        from lib.models.magazine import Magazine
        results = self._execute_query(
            """
            SELECT DISTINCT m.* FROM magazines m
            JOIN articles a ON m.id = a.magazine_id
            WHERE a.author_id = ?
            """,
            (self.id,),
            fetch_all=True
        )
        return [Magazine(**row) for row in results]

    def add_article(self, magazine, title):
        """Add a new article for this author"""
        from lib.models.article import Article
        if not self.id or not magazine.id or not title:
            raise ValueError("Author, magazine, and title must be provided")
        return Article(title=title, author_id=self.id, magazine_id=magazine.id).save()

    def topic_areas(self):
        """Get unique categories of magazines this author has written for"""
        results = self._execute_query(
            """
            SELECT DISTINCT m.category FROM magazines m
            JOIN articles a ON m.id = a.magazine_id
            WHERE a.author_id = ?
            """,
            (self.id,),
            fetch_all=True
        )
        return [row['category'] for row in results]

    def __repr__(self):
        return f"<Author id={self.id} name='{self.name}'>"