import os
os.environ['TESTING'] = '1'
import pytest
from lib.models.article import Article
from lib.models.author import Author
from lib.models.magazine import Magazine

@pytest.fixture(autouse=True)
def setup_db():
    """Setup and teardown for each test"""
    from lib.db.connection import setup_database
    from lib.models import BaseModel
    
    # Clear existing tables
    BaseModel._execute_query("DROP TABLE IF EXISTS articles", commit=True)
    BaseModel._execute_query("DROP TABLE IF EXISTS authors", commit=True)
    BaseModel._execute_query("DROP TABLE IF EXISTS magazines", commit=True)
    
    # Recreate tables
    setup_database()
    
    # Seed test data
    from lib.db.seed import seed_database
    seed_database()
    
    yield
    
    # No teardown needed since we're using an in-memory database for tests

def test_article_creation():
    author = Author.find_by_name("John Doe")[0]
    magazine = Magazine.find_by_name("Tech Today")[0]
    article = Article(title="Test Article", author_id=author.id, magazine_id=magazine.id).save()
    assert article.id is not None
    assert article.title == "Test Article"

def test_article_relationships():
    article = Article.find_by_title("Python Programming")[0]
    author = article.author()
    magazine = article.magazine()
    assert author is not None
    assert magazine is not None
    assert isinstance(author, Author)
    assert isinstance(magazine, Magazine)