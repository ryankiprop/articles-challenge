from lib.models import BaseModel

class Magazine(BaseModel):
    TABLE_NAME = "magazines"

    def __init__(self, id=None, name=None, category=None):
        self.id = id
        self.name = name
        self.category = category

    def save(self):
        """Save the magazine to the database"""
        if not self.name or not self.category:
            raise ValueError("Magazine name and category cannot be empty")

        if self.id:
            query = "UPDATE magazines SET name = ?, category = ? WHERE id = ?"
            params = (self.name, self.category, self.id)
        else:
            query = "INSERT INTO magazines (name, category) VALUES (?, ?) RETURNING id"
            params = (self.name, self.category)

        result = self._execute_query(query, params, fetch_one=True, commit=True)
        if not self.id:
            self.id = result[0]
        return self

    def delete(self):
        """Delete the magazine from the database"""
        if self.id:
            self._execute_query(
                "DELETE FROM magazines WHERE id = ?",
                (self.id,),
                commit=True
            )

    @classmethod
    def find_by_id(cls, id):
        """Find a magazine by ID"""
        result = cls._execute_query(
            "SELECT * FROM magazines WHERE id = ?",
            (id,),
            fetch_one=True
        )
        return cls(**result) if result else None

    @classmethod
    def find_by_name(cls, name):
        """Find magazines by name"""
        results = cls._execute_query(
            "SELECT * FROM magazines WHERE name = ?",
            (name,),
            fetch_all=True
        )
        return [cls(**row) for row in results]

    @classmethod
    def find_by_category(cls, category):
        """Find magazines by category"""
        results = cls._execute_query(
            "SELECT * FROM magazines WHERE category = ?",
            (category,),
            fetch_all=True
        )
        return [cls(**row) for row in results]

    @classmethod
    def get_all(cls):
        """Get all magazines"""
        results = cls._execute_query("SELECT * FROM magazines", fetch_all=True)
        return [cls(**row) for row in results]

    def articles(self):
        """Get all articles published in this magazine"""
        from lib.models.article import Article
        results = self._execute_query(
            "SELECT * FROM articles WHERE magazine_id = ?",
            (self.id,),
            fetch_all=True
        )
        return [Article(**row) for row in results]

    def contributors(self):
        """Get all authors who have written for this magazine"""
        from lib.models.author import Author
        results = self._execute_query(
            """
            SELECT DISTINCT a.* FROM authors a
            JOIN articles ar ON a.id = ar.author_id
            WHERE ar.magazine_id = ?
            """,
            (self.id,),
            fetch_all=True
        )
        return [Author(**row) for row in results]

    def article_titles(self):
        """Get titles of all articles in this magazine"""
        results = self._execute_query(
            "SELECT title FROM articles WHERE magazine_id = ?",
            (self.id,),
            fetch_all=True
        )
        return [row['title'] for row in results]

    def contributing_authors(self):
        """Get authors with more than 2 articles in this magazine"""
        from lib.models.author import Author
        results = self._execute_query(
            """
            SELECT a.*, COUNT(ar.id) as article_count FROM authors a
            JOIN articles ar ON a.id = ar.author_id
            WHERE ar.magazine_id = ?
            GROUP BY a.id HAVING COUNT(ar.id) > 2
            """,
            (self.id,),
            fetch_all=True
        )
        return [Author(**row) for row in results]

    @classmethod
    def top_publisher(cls):
        """Get the magazine with the most articles"""
        result = cls._execute_query(
            """
            SELECT m.*, COUNT(a.id) as article_count FROM magazines m
            LEFT JOIN articles a ON m.id = a.magazine_id
            GROUP BY m.id ORDER BY article_count DESC LIMIT 1
            """,
            fetch_one=True
        )
        return cls(**result) if result else None

    def __repr__(self):
        return f"<Magazine id={self.id} name='{self.name}' category='{self.category}'>"