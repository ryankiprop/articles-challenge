from lib.models.author import Author
from lib.models.magazine import Magazine
from lib.models.article import Article

def run_example_queries():
    print("Running example queries...\n")
    
    # 1. Get all articles written by a specific author
    author = Author.find_by_name("John Doe")[0]
    print(f"Articles by {author.name}:")
    for article in author.articles():
        print(f"  - {article.title}")
    
    # 2. Find all magazines a specific author has contributed to
    print(f"\nMagazines {author.name} has contributed to:")
    for magazine in author.magazines():
        print(f"  - {magazine.name} ({magazine.category})")
    
    # 3. Get all authors who have written for a specific magazine
    magazine = Magazine.find_by_name("Tech Today")[0]
    print(f"\nAuthors who have written for {magazine.name}:")
    for contributor in magazine.contributors():
        print(f"  - {contributor.name}")
    
    # 4. Find magazines with articles by at least 2 different authors
    print("\nMagazines with articles by at least 2 authors:")
    all_mags = Magazine.get_all()
    for mag in all_mags:
        contributors = mag.contributors()
        if len(contributors) >= 2:
            print(f"  - {mag.name} has {len(contributors)} contributors")
    
    # 5. Count the number of articles in each magazine
    print("\nArticle count per magazine:")
    for mag in all_mags:
        count = len(mag.articles())
        print(f"  - {mag.name}: {count} articles")
    
    # 6. Find the author who has written the most articles
    authors = Author.get_all()
    top_author = max(authors, key=lambda a: len(a.articles()))
    print(f"\nTop author: {top_author.name} with {len(top_author.articles())} articles")
    
    # Bonus: Magazine with most articles
    top_mag = Magazine.top_publisher()
    print(f"\nTop publisher magazine: {top_mag.name} with {len(top_mag.articles())} articles")

if __name__ == '__main__':
    run_example_queries()