from lib.models.author import Author
from lib.models.magazine import Magazine
from lib.models.article import Article

def seed_database():
    # Clear existing data
    Author.drop_table()
    Magazine.drop_table()
    Article.drop_table()
    
    # Recreate tables
    Author.create_table()
    Magazine.create_table()
    Article.create_table()
    
    # Create authors
    authors = [
        Author.create("John Doe"),
        Author.create("Jane Smith"),
        Author.create("Robert Johnson"),
        Author.create("Emily Davis")
    ]
    
    # Create magazines
    magazines = [
        Magazine.create("Tech Today", "Technology"),
        Magazine.create("Science Weekly", "Science"),
        Magazine.create("Business Insights", "Business"),
        Magazine.create("Creative Writing", "Literature")
    ]
    
    # Create articles
    articles = [
        {"title": "Python Programming", "author": 0, "magazine": 0},
        {"title": "Machine Learning", "author": 0, "magazine": 0},
        {"title": "Quantum Physics", "author": 1, "magazine": 1},
        {"title": "Neuroscience", "author": 1, "magazine": 1},
        {"title": "Stock Market", "author": 2, "magazine": 2},
        {"title": "Startup Funding", "author": 0, "magazine": 2},
        {"title": "AI Ethics", "author": 1, "magazine": 0},
        {"title": "Blockchain", "author": 2, "magazine": 0},
        {"title": "Modern Poetry", "author": 3, "magazine": 3},
        {"title": "Short Stories", "author": 3, "magazine": 3}
    ]
    
    for article in articles:
        Article.create(
            title=article["title"],
            author_id=authors[article["author"]].id,
            magazine_id=magazines[article["magazine"]].id
        )

if __name__ == '__main__':
    seed_database()
    print("Database seeded successfully!")