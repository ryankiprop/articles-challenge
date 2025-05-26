import pytest
from lib.models.author import Author
from lib.models.magazine import Magazine
from lib.models.article import Article
from lib.db.connection import get_connection

@pytest.fixture(autouse=True)
def setup_db():
    """Setup and teardown for each test"""
    from lib.db.seed import seed_database
    seed_database()
    yield
    # Clean up after tests

def test_author_creation():
    author = Author(name="Test Author").save()
    assert author.id is not None
    assert author.name == "Test Author"

def test_author_articles():
    author = Author.find_by_name("John Doe")[0]
    articles = author.articles()
    assert len(articles) >= 2
    assert all(article.author_id == author.id for article in articles)

def test_author_magazines():
    author = Author.find_by_name("John Doe")[0]
    magazines = author.magazines()
    assert len(magazines) >= 2
    assert all(isinstance(m, Magazine) for m in magazines)

def test_author_topic_areas():
    author = Author.find_by_name("John Doe")[0]
    topics = author.topic_areas()
    assert len(topics) >= 1
    assert all(isinstance(t, str) for t in topics)