from lib.models.author import Author
from lib.models.magazine import Magazine
from lib.models.article import Article

def run():
    print("\nAll authors:")
    authors = Author.all()
    for a in authors:
        print(f"{a.id}: {a.name}")

    print("\nAll magazines:")
    magazines = Magazine.all()
    for m in magazines:
        print(f"{m.id}: {m.name} ({m.category})")

    print("\nAll articles:")
    articles = Article.all()
    for art in articles:
        print(f"{art.id}: {art.title}")

    author = authors[0]
    print(f"\nArticles by {author.name}:")
    for a in author.articles():
        print(f"- {a['title']}")

    print(f"\nMagazines {author.name} contributed to:")
    for m in author.magazines():
        print(f"- {m['name']}")

    magazine = magazines[0]
    print(f"\nContributors to {magazine.name}:")
    for a in magazine.contributors():
        print(f"- {a.name}")

    print(f"\nTop contributing authors in {magazine.name}:")
    for a in magazine.contributing_authors():
        print(f"- {a.name}")

if __name__ == "__main__":
    run()
