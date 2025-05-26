from lib.models.author import Author
from lib.models.magazine import Magazine
from lib.models.article import Article
from lib.db.seed import seed_database

def reset_database():
    """Reset and seed the database"""
    seed_database()
    print("Database reset complete!")

def print_all_data():
    """Print all data in the database"""
    print("\nAuthors:")
    for author in Author.get_all():
        print(f"  {author}")
    
    print("\nMagazines:")
    for magazine in Magazine.get_all():
        print(f"  {magazine}")
    
    print("\nArticles:")
    for article in Article.get_all():
        print(f"  {article}")

if __name__ == '__main__':
    reset_database()
    print("\nInteractive debug session started.")
    print("Available classes: Author, Magazine, Article")
    print("Helper functions: reset_database(), print_all_data()")