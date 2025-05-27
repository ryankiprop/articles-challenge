import pytest
from lib.models.magazine import Magazine
from lib.models.author import Author
from lib.models.article import Article

def test_magazine_creation():
    magazine = Magazine.create("Test Magazine", "Lifestyle")
    assert magazine.name == "Test Magazine"
    assert magazine.category == "Lifestyle"

def test_magazine_articles_and_contributors():
    mag = Magazine.create("Mag With Articles", "Tech")
    author = Author.create("Author One")
    article = author.add_article(mag, "Mag Article", "Some content")
    articles = mag.articles()
    contributors = mag.contributors()
    assert len(articles) > 0
    assert len(contributors) > 0
    assert articles[0].title == "Mag Article"
    assert contributors[0].name == "Author One"

def test_magazine_article_titles_and_contributing_authors():
    mag = Magazine.create("Title Test Mag", "Science")
    author = Author.create("Author Two")
    article = author.add_article(mag, "Title Test Article", "Content here")
    titles = mag.article_titles()
    authors = mag.contributing_authors()
    assert "Title Test Article" in titles
    assert any(a.name == "Author Two" for a in authors)
