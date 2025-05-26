from lib.models import BaseModel

class Article(BaseModel):
    TABLE_NAME = "articles"

    def __init__(self, id=None, title=None, author_id=None, magazine_id=None):
        self.id = id
        self.title = title
        self.author_id = author_id
        self.magazine_id = magazine_id

    def save(self):
        """Save the article to the database"""
        if not self.title or not self.author_id or not self.magazine_id:
            raise ValueError("Article title, author_id, and magazine_id are required")

        if self.id:
            query = """
                UPDATE articles 
                SET title = ?, author_id = ?, magazine_id = ? 
                WHERE id = ?
            """
            params = (self.title, self.author_id, self.magazine_id, self.id)
        else:
            query = """
                INSERT INTO articles (title, author_id, magazine_id)
                VALUES (?, ?, ?) RETURNING id
            """
            params = (self.title, self.author_id, self.magazine_id)

        result = self._execute_query(query, params, fetch_one=True, commit=True)
        if not self.id:
            self.id = result[0]
        return self

    def delete(self):
        """Delete the article from the database"""
        if self.id:
            self._execute_query(
                "DELETE FROM articles WHERE id = ?",
                (self.id,),
                commit=True
            )

    @classmethod
    def find_by_id(cls, id):
        """Find an article by ID"""
        result = cls._execute_query(
            "SELECT * FROM articles WHERE id = ?",
            (id,),
            fetch_one=True
        )
        return cls(**result) if result else None

    @classmethod
    def find_by_title(cls, title):
        """Find articles by title"""
        results = cls._execute_query(
            "SELECT * FROM articles WHERE title = ?",
            (title,),
            fetch_all=True
        )
        return [cls(**row) for row in results]

    @classmethod
    def find_by_author(cls, author_id):
        """Find articles by author ID"""
        results = cls._execute_query(
            "SELECT * FROM articles WHERE author_id = ?",
            (author_id,),
            fetch_all=True
        )
        return [cls(**row) for row in results]

    @classmethod
    def find_by_magazine(cls, magazine_id):
        """Find articles by magazine ID"""
        results = cls._execute_query(
            "SELECT * FROM articles WHERE magazine_id = ?",
            (magazine_id,),
            fetch_all=True
        )
        return [cls(**row) for row in results]

    @classmethod
    def get_all(cls):
        """Get all articles"""
        results = cls._execute_query("SELECT * FROM articles", fetch_all=True)
        return [cls(**row) for row in results]

    def author(self):
        """Get the author of this article"""
        from lib.models.author import Author
        return Author.find_by_id(self.author_id)

    def magazine(self):
        """Get the magazine of this article"""
        from lib.models.magazine import Magazine
        return Magazine.find_by_id(self.magazine_id)

    def __repr__(self):
        return f"<Article id={self.id} title='{self.title}' author_id={self.author_id} magazine_id={self.magazine_id}>"