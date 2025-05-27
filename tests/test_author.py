import pytest
from lib.models.author import Author
from lib.models.magazine import Magazine
from lib.models.article import Article

def test_author_creation():
    author = Author.create("Test Author")
    assert author.name == "Test Author"

def test_author_articles_and_magazines():
    author = Author.create("Auth Articles Magazines")
    magazine = Magazine.create("Test Mag", "Health")
    article = author.add_article(magazine, "Author Article", "Article content here")
    articles = author.articles()
    magazines = author.magazines()
    assert len(articles) > 0
    assert len(magazines) > 0
    assert articles[0].title == "Author Article"
    assert magazines[0].name == "Test Mag"

def test_add_article_and_topic_areas():
    author = Author.create("Temp Author")
    mag = Magazine.create("TestMag", "Science")
    article = author.add_article(mag, "Test Article", "Content for test article")
    assert article.title == "Test Article"
    assert article.content == "Content for test article"
