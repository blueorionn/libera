"""Load book data into the database.

Usage::

    DB_URI="mysql+pymysql://..." python scripts/load_data.py
"""

import os
import sys
from urllib.parse import quote_plus

from sqlalchemy import create_engine
from sqlalchemy.orm import Session

# -- Make the project root importable ----------------------------------------
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from libera.models import Base, Book  # noqa: E402

# -- Book seed data (17 books) -----------------------------------------------

SEED_BOOKS = [
    Book(
        id="e8c7c561-bc25-46f2-8b27-5ea8d42a9c5e",
        title="Harry Potter and the Sorcerer's Stone",
        summary="Harry Potter, an orphan living with his cruel Muggle (non-magical) "
        "relatives, discovers that he is a wizard. He begins attending "
        "Hogwarts School of Witchcraft and Wizardry, where he makes friends "
        "with Ron Weasley and Hermione Granger. Together, they embark on a "
        "journey to uncover the truth about the Sorcerer's Stone, a powerful "
        "object that can grant eternal life.",
        ISBN=9780439554930,
        genre="Fantasy, Magic",
        publication_year=1997,
        author="J.K. Rowling",
        publisher="Scholastic",
        rating=4.4,
    ),
    Book(
        id="26e3e8a8-a882-4a97-b06a-48c4b2f7eac6",
        title="To Kill a Mockingbird",
        summary="Set in the Deep South during the 1930s, this Pulitzer Prize-winning "
        "novel follows a young girl's experience of racial injustice in a "
        "small Alabama town. As she witnesses her father, a lawyer, defend a "
        "wrongly accused black man, she learns valuable lessons about "
        "prejudice, empathy, and understanding.",
        ISBN=9780061120084,
        genre="Fiction, Classics",
        publication_year=1960,
        author="Harper Lee",
        publisher="J.B. Lippincott & Co.",
        rating=4.7,
    ),
    Book(
        id="b6a7c3b6-2398-49c1-a6c0-4ee7a5e7bfc0",
        title="The Invisible Man",
        summary="This masterpiece of science fiction is the fascinating story of "
        "Griffin, a scientist who creates a serum to render himself "
        "invisible, and his descent into madness that follows.",
        ISBN=9780486284728,
        genre="Science Fiction, Classics",
        publication_year=1897,
        author="H.G. Wells",
        publisher="Pearson's Magazine",
        rating=4.1,
    ),
    Book(
        id="7bab5cff-6b86-4027-891e-b41441261b9e",
        title="The Nightingale",
        summary="Set in France during World War II, this historical fiction novel "
        "tells the story of two sisters, Vianne and Isabelle, as they "
        "navigate the difficulties and dangers of living under German "
        "occupation. While Vianne tries to maintain a sense of normalcy and "
        "protect her young daughter, Isabelle joins the French Resistance, "
        "risking everything to fight against the Nazis.",
        ISBN=9781250066197,
        genre="Historical Fiction, War",
        publication_year=2015,
        author="Kristin Hannah",
        publisher="St. Martin's Press",
        rating=4.8,
    ),
    Book(
        id="f2541876-7025-4bb1-ac7c-e30f664ed919",
        title="The Hitchhiker's Guide to the Galaxy",
        summary="When Earth is destroyed to make way for a hyperspace bypass, "
        "unwitting human Arthur Dent hitches a ride on a passing spaceship. "
        "He embarks on a misadventure-filled journey through space and time, "
        "accompanied by his friend Ford Prefect, an alien researching Earth "
        "for the titular guidebook.",
        ISBN=9781400052929,
        genre="Science Fiction, Comedy",
        publication_year=1979,
        author="Douglas Adams",
        publisher="Pan Books",
        rating=4.4,
    ),
    Book(
        id="7a2f9c3e-4b8d-4f61-9c2e-5d8a1b3c7e4f",
        title="1984",
        summary="In a dystopian future ruled by the omnipresent Big Brother, "
        "Winston Smith works at the Ministry of Truth rewriting historical "
        "records to match the Party's ever-changing narrative. His secret "
        "rebellion and forbidden love affair with Julia draw him into a "
        "confrontation with the totalitarian state, in a chilling exploration "
        "of surveillance, censorship, and individual freedom.",
        ISBN=9780451524935,
        genre="Dystopian, Classics",
        publication_year=1949,
        author="George Orwell",
        publisher="Signet Classic",
        rating=4.6,
    ),
    Book(
        id="3d6e8b1a-9c2f-4e7d-8b3a-1f4c9d6e2b7a",
        title="The Great Gatsby",
        summary="Set in the glittering Jazz Age of 1920s New York, this American "
        "classic follows the enigmatic millionaire Jay Gatsby and his "
        "obsessive pursuit of the beautiful Daisy Buchanan. Through the eyes "
        "of narrator Nick Carraway, the novel reveals the corruption beneath "
        "the era's glamour and ends in one of literature's most famous "
        "tragedies.",
        ISBN=9780743273565,
        genre="Fiction, Classics",
        publication_year=1925,
        author="F. Scott Fitzgerald",
        publisher="Scribner",
        rating=4.2,
    ),
    Book(
        id="c5a9e2d4-7b3f-4a8c-9d1e-6f2b4c8a3e5d",
        title="Pride and Prejudice",
        summary="Elizabeth Bennet, the witty and independent second daughter of "
        "the Bennet family, clashes with the proud and wealthy Mr. Darcy in "
        "this beloved Regency-era romance. Through sharp social commentary "
        "and sparkling dialogue, Jane Austen crafts a timeless story of "
        "first impressions, family expectations, and love that overcomes "
        "pride and prejudice.",
        ISBN=9780141439518,
        genre="Romance, Classics",
        publication_year=1813,
        author="Jane Austen",
        publisher="Penguin Classics",
        rating=4.5,
    ),
    Book(
        id="8f1c4b7e-2d6a-4e9b-8c3f-5a7d2e9b1c4f",
        title="The Catcher in the Rye",
        summary="Disillusioned teenager Holden Caulfield recounts three restless "
        "days in New York City after being expelled from prep school. His "
        "cynical observations of what he calls the 'phony' adult world and "
        "his longing to protect childhood innocence made this novel a "
        "defining voice of postwar American adolescence.",
        ISBN=9780316769488,
        genre="Fiction, Classics",
        publication_year=1951,
        author="J.D. Salinger",
        publisher="Little, Brown and Company",
        rating=4.0,
    ),
    Book(
        id="1b7d3f9a-5c2e-4b8d-9a6f-3e1c7b5d2a9f",
        title="The Fellowship of the Ring",
        summary="The first volume of J.R.R. Tolkien's epic The Lord of the Rings "
        "follows young hobbit Frodo Baggins, who inherits the One Ring, an "
        "artifact of immense power that must be destroyed in the fires of "
        "Mount Doom. He and the Fellowship of nine companions set out across "
        "Middle-earth, pursued by the dark forces of the fallen Maia Sauron.",
        ISBN=9780547928210,
        genre="Fantasy, Adventure",
        publication_year=1954,
        author="J.R.R. Tolkien",
        publisher="Mariner Books",
        rating=4.7,
    ),
    Book(
        id="4e6c2a8d-9f3b-4d7c-8e1a-2b5f9c4d6e3a",
        title="The Hobbit",
        summary="Bilbo Baggins, a comfortable and unadventurous hobbit, is swept "
        "into an epic quest when the wizard Gandalf and thirteen dwarves "
        "arrive at his door, seeking to reclaim their stolen treasure from "
        "the dragon Smaug. Along the way, Bilbo discovers courage he never "
        "knew he had and comes into possession of a mysterious ring.",
        ISBN=9780547928227,
        genre="Fantasy, Adventure",
        publication_year=1937,
        author="J.R.R. Tolkien",
        publisher="Mariner Books",
        rating=4.6,
    ),
    Book(
        id="2a8f5d1c-7b4e-4c9a-8d3f-6e1b9a4c7f2d",
        title="The Da Vinci Code",
        summary="Harvard symbologist Robert Langdon is summoned to the Louvre "
        "after the murder of a curator, whose body is found surrounded by "
        "cryptic symbols. Teaming up with cryptologist Sophie Neveu, "
        "Langdon uncovers a centuries-old conspiracy involving the Holy "
        "Grail, secret societies, and hidden messages in Leonardo da Vinci's "
        "masterpieces.",
        ISBN=9780307474278,
        genre="Thriller, Mystery",
        publication_year=2003,
        author="Dan Brown",
        publisher="Anchor Books",
        rating=3.9,
    ),
    Book(
        id="9d3b7e2f-1c6a-4f8d-8b2e-5c4a9f1d7e3b",
        title="The Hunger Games",
        summary="In the dystopian nation of Panem, sixteen-year-old Katniss "
        "Everdeen volunteers to take her younger sister's place in the "
        "annual Hunger Games, a televised fight to the death between "
        "tributes from the twelve districts. Her defiance inside the arena "
        "ignites a spark of rebellion that threatens to engulf the entire "
        "nation.",
        ISBN=9780439023528,
        genre="Dystopian, Young Adult",
        publication_year=2008,
        author="Suzanne Collins",
        publisher="Scholastic",
        rating=4.3,
    ),
    Book(
        id="6f1e9c4b-3a8d-4b7f-9e2c-1d5a8f3b6e4c",
        title="Gone Girl",
        summary="On their fifth wedding anniversary, Nick Dunne's wife Amy "
        "vanishes under suspicious circumstances, and the mounting evidence "
        "points squarely at him. Alternating between Nick's present-day "
        "account and Amy's diary entries, this psychological thriller "
        "delivers one of the most shocking twists in modern crime fiction.",
        ISBN=9780307588371,
        genre="Thriller, Mystery",
        publication_year=2012,
        author="Gillian Flynn",
        publisher="Crown Publishing Group",
        rating=4.1,
    ),
    Book(
        id="b4d2a8f6-5e9c-4a3d-8f7b-2c6e1a9d4f3b",
        title="The Kite Runner",
        summary="Amir, a privileged boy from Kabul, and Hassan, the son of his "
        "father's servant, grow up inseparable until a single act of "
        "cowardice shatters their friendship. Years later, living in "
        "America, Amir returns to a war-torn Afghanistan to confront the "
        "past and seek the redemption he has long avoided.",
        ISBN=9781594480003,
        genre="Historical Fiction, Drama",
        publication_year=2003,
        author="Khaled Hosseini",
        publisher="Riverhead Books",
        rating=4.5,
    ),
    Book(
        id="7e3c9f1a-2b6d-4e8a-9c4f-5d2b8a1e7f3c",
        title="The Alchemist",
        summary="Andalusian shepherd boy Santiago follows his recurring dream of "
        "treasure hidden near the Egyptian pyramids, leaving behind "
        "everything he knows to journey across the desert. Guided by a "
        "series of mentors, he learns to listen to his heart and pursue his "
        "Personal Legend, in this timeless fable about following one's "
        "dreams.",
        ISBN=9780062315007,
        genre="Fiction, Inspirational",
        publication_year=1988,
        author="Paulo Coelho",
        publisher="HarperOne",
        rating=4.2,
    ),
    Book(
        id="5a1d7b3f-8c4e-4f2a-8d6b-3e9c1f5a7d2b",
        title="The Martian",
        summary="When a fierce dust storm forces his crew to abandon Mars, "
        "astronaut Mark Watney is left behind, presumed dead. Stranded with "
        "limited supplies, he must rely on his ingenuity, botany skills, "
        "and sharp humor to survive on a hostile planet until a rescue "
        "mission can reach him.",
        ISBN=9780553418026,
        genre="Science Fiction, Adventure",
        publication_year=2014,
        author="Andy Weir",
        publisher="Broadway Books",
        rating=4.5,
    ),
]


def _get_engine():
    """Return a SQLAlchemy engine, resolving DB_URI from the environment."""
    db_uri = os.environ.get("DB_URI", "")
    if not db_uri:
        host = os.environ.get("DB_HOST", "")
        port = os.environ.get("DB_PORT", "3306")
        user = os.environ.get("DB_USER", "")
        password = os.environ.get("DB_PASSWORD", "")
        name = os.environ.get("DB_NAME", "")
        if user and name and host:
            db_uri = (
                f"mysql+pymysql://{user}:{quote_plus(password)}"
                f"@{host}:{port}/{name}"
            )
        else:
            db_uri = "sqlite:///data.db"

    return create_engine(db_uri, echo=False)


def main():
    engine = _get_engine()

    # Ensure tables exist.
    Base.metadata.create_all(engine)

    with Session(engine) as session:
        if session.query(Book).count() == 0:
            session.add_all(SEED_BOOKS)
            session.commit()
            print(f"Inserted {len(SEED_BOOKS)} books.")
        else:
            print("Books already loaded — skipping.")

    engine.dispose()


if __name__ == "__main__":
    main()
