from lib.models.author import Author
from lib.models.magazine import Magazine

alice = Author.create("Alice")
bob = Author.create("Bob")
carol = Author.create("Carol")

tech_mag = Magazine.create("Tech Weekly", "Technology")
health_mag = Magazine.create("Health Matters", "Health")

alice.add_article(tech_mag, "AI in 2025")
alice.add_article(health_mag, "Mental Health Tips")
bob.add_article(tech_mag, "The Rise of Python")
bob.add_article(tech_mag, "Cloud Computing Basics")
carol.add_article(tech_mag, "Cybersecurity Trends")
carol.add_article(health_mag, "Nutrition Facts")
carol.add_article(health_mag, "Exercise for Longevity")
