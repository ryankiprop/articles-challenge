import pytest
from lib.models.magazine import Magazine
from lib.models.author import Author

@pytest.fixture(autouse=True)
def setup_db():
    """Setup and teardown for each test"""
    from lib.db.seed import seed_database
    seed_database()
    yield
    # Clean up after tests

def test_magazine_creation():
    magazine = Magazine(name="Test Magazine", category="Test").save()
    assert magazine.id is not None
    assert magazine.name == "Test Magazine"

def test_magazine_articles():
    magazine = Magazine.find_by_name("Tech Today")[0]
    articles = magazine.articles()
    assert len(articles) >= 2
    assert all(article.magazine_id == magazine.id for article in articles)

def test_magazine_contributors():
    magazine = Magazine.find_by_name("Tech Today")[0]
    contributors = magazine.contributors()
    assert len(contributors) >= 2
    assert all(isinstance(c, Author) for c in contributors)

def test_top_publisher():
    top_mag = Magazine.top_publisher()
    assert top_mag is not None
    assert isinstance(top_mag, Magazine)