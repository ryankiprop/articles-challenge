import pytest
from lib.models.article import Article
from lib.models.author import Author
from lib.models.magazine import Magazine

def test_article_creation():
    author = Author.create("Article Author")
    magazine = Magazine.create("Article Mag", "Tech")
    article = Article.create("Tech Article", author.id, magazine.id, "Article body here")
    assert article.title == "Tech Article"
    assert article.author_id == author.id
    assert article.magazine_id == magazine.id
    assert article.content == "Article body here"

def test_find_article_by_id():
    author = Author.create("Find Author")
    magazine = Magazine.create("Find Mag", "Science")
    article = Article.create("Find Article", author.id, magazine.id, "Content to find")
    found_article = Article.find_by_id(article.id)
    assert found_article is not None
    assert found_article.title == "Find Article"
    assert found_article.content == "Content to find"
