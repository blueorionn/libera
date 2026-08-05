"""Standalone script to load data to sqldb."""

import os
import sys
import mysql.connector
from urllib.parse import urlparse


def _parse_db_connection():
    """Parse DB_URI env var (or fall back to individual DB_* vars).

    Returns a dict with keys: host, port, user, password, name
    """
    db_uri = os.environ.get("DB_URI", "")
    if db_uri:
        parsed = urlparse(db_uri)
        return {
            "host": parsed.hostname or "localhost",
            "port": parsed.port or 3306,
            "user": parsed.username or "",
            "password": parsed.password or "",
            "name": parsed.path.lstrip("/") or "",
        }

    # Fallback to individual vars
    host = os.environ.get("DB_HOST") or ""
    name = os.environ.get("DB_NAME") or ""
    user = os.environ.get("DB_USER") or ""
    password = os.environ.get("DB_PASSWORD") or ""
    port = os.environ.get("DB_PORT") or 3306

    if not host:
        raise ValueError("DB_URI not set and DB_HOST is empty")
    if not name:
        raise ValueError("DB_URI not set and DB_NAME is empty")
    if not user:
        raise ValueError("DB_URI not set and DB_USER is empty")

    return {
        "host": host,
        "port": int(port),
        "user": user,
        "password": password,
        "name": name,
    }


def create_book_query():
    query = """
        CREATE TABLE
            IF NOT EXISTS books (
                id VARCHAR(36) PRIMARY KEY,
                title VARCHAR(255) UNIQUE,
                summary TEXT,
                ISBN BIGINT UNSIGNED,
                genre VARCHAR(255),
                publication_year INT UNSIGNED,
                author VARCHAR(255),
                publisher VARCHAR(255) NULL,
                rating FLOAT
            )
    """

    return query


def insert_books_query():
    query = """

INSERT INTO
    books (
        id,
        title,
        summary,
        ISBN,
        genre,
        publication_year,
        author,
        publisher,
        rating
    )
VALUES
    (
        'e8c7c561-bc25-46f2-8b27-5ea8d42a9c5e',
        'Harry Potter and the Sorcerer''s Stone',
        'Harry Potter, an orphan living with his cruel Muggle (non-magical) relatives, discovers that he is a wizard. He begins attending Hogwarts School of Witchcraft and Wizardry, where he makes friends with Ron Weasley and Hermione Granger. Together, they embark on a journey to uncover the truth about the Sorcerer''s Stone, a powerful object that can grant eternal life.',
        9780439554930,
        'Fantasy, Magic',
        1997,
        'J.K. Rowling',
        'Scholastic',
        4.4
    ),
    (
        '26e3e8a8-a882-4a97-b06a-48c4b2f7eac6',
        'To Kill a Mockingbird',
        'Set in the Deep South during the 1930s, this Pulitzer Prize-winning novel follows a young girl''s experience of racial injustice in a small Alabama town. As she witnesses her father, a lawyer, defend a wrongly accused black man, she learns valuable lessons about prejudice, empathy, and understanding.',
        9780061120084,
        'Fiction, Classics',
        1960,
        'Harper Lee',
        'J.B. Lippincott & Co.',
        4.7
    ),
    (
        'b6a7c3b6-2398-49c1-a6c0-4ee7a5e7bfc0',
        'The Invisible Man',
        'This masterpiece of science fiction is the fascinating story of Griffin, a scientist who creates a serum to render himself invisible, and his descent into madness that follows.',
        9780486284728,
        'Science Fiction, Classics',
        1897,
        'H.G. Wells',
        'Pearson''s Magazine',
        4.1
    ),
    (
        '7bab5cff-6b86-4027-891e-b41441261b9e',
        'The Nightingale',
        'Set in France during World War II, this historical fiction novel tells the story of two sisters, Vianne and Isabelle, as they navigate the difficulties and dangers of living under German occupation. While Vianne tries to maintain a sense of normalcy and protect her young daughter, Isabelle joins the French Resistance, risking everything to fight against the Nazis.',
        9781250066197,
        'Historical Fiction, War',
        2015,
        'Kristin Hannah',
        'St. Martin''s Press',
        4.8
    ),
    (
        'f2541876-7025-4bb1-ac7c-e30f664ed919',
        'The Hitchhiker''s Guide to the Galaxy',
        'When Earth is destroyed to make way for a hyperspace bypass, unwitting human Arthur Dent hitches a ride on a passing spaceship. He embarks on a misadventure-filled journey through space and time, accompanied by his friend Ford Prefect, an alien researching Earth for the titular guidebook.',
        9781400052929,
        'Science Fiction, Comedy',
        1979,
        'Douglas Adams',
        'Pan Books',
        4.4
    ),
    (
        '7a2f9c3e-4b8d-4f61-9c2e-5d8a1b3c7e4f',
        '1984',
        'In a dystopian future ruled by the omnipresent Big Brother, Winston Smith works at the Ministry of Truth rewriting historical records to match the Party''s ever-changing narrative. His secret rebellion and forbidden love affair with Julia draw him into a confrontation with the totalitarian state, in a chilling exploration of surveillance, censorship, and individual freedom.',
        9780451524935,
        'Dystopian, Classics',
        1949,
        'George Orwell',
        'Signet Classic',
        4.6
    ),
    (
        '3d6e8b1a-9c2f-4e7d-8b3a-1f4c9d6e2b7a',
        'The Great Gatsby',
        'Set in the glittering Jazz Age of 1920s New York, this American classic follows the enigmatic millionaire Jay Gatsby and his obsessive pursuit of the beautiful Daisy Buchanan. Through the eyes of narrator Nick Carraway, the novel reveals the corruption beneath the era''s glamour and ends in one of literature''s most famous tragedies.',
        9780743273565,
        'Fiction, Classics',
        1925,
        'F. Scott Fitzgerald',
        'Scribner',
        4.2
    ),
    (
        'c5a9e2d4-7b3f-4a8c-9d1e-6f2b4c8a3e5d',
        'Pride and Prejudice',
        'Elizabeth Bennet, the witty and independent second daughter of the Bennet family, clashes with the proud and wealthy Mr. Darcy in this beloved Regency-era romance. Through sharp social commentary and sparkling dialogue, Jane Austen crafts a timeless story of first impressions, family expectations, and love that overcomes pride and prejudice.',
        9780141439518,
        'Romance, Classics',
        1813,
        'Jane Austen',
        'Penguin Classics',
        4.5
    ),
    (
        '8f1c4b7e-2d6a-4e9b-8c3f-5a7d2e9b1c4f',
        'The Catcher in the Rye',
        'Disillusioned teenager Holden Caulfield recounts three restless days in New York City after being expelled from prep school. His cynical observations of what he calls the ''phony'' adult world and his longing to protect childhood innocence made this novel a defining voice of postwar American adolescence.',
        9780316769488,
        'Fiction, Classics',
        1951,
        'J.D. Salinger',
        'Little, Brown and Company',
        4.0
    ),
    (
        '1b7d3f9a-5c2e-4b8d-9a6f-3e1c7b5d2a9f',
        'The Fellowship of the Ring',
        'The first volume of J.R.R. Tolkien''s epic The Lord of the Rings follows young hobbit Frodo Baggins, who inherits the One Ring, an artifact of immense power that must be destroyed in the fires of Mount Doom. He and the Fellowship of nine companions set out across Middle-earth, pursued by the dark forces of the fallen Maia Sauron.',
        9780547928210,
        'Fantasy, Adventure',
        1954,
        'J.R.R. Tolkien',
        'Mariner Books',
        4.7
    ),
    (
        '4e6c2a8d-9f3b-4d7c-8e1a-2b5f9c4d6e3a',
        'The Hobbit',
        'Bilbo Baggins, a comfortable and unadventurous hobbit, is swept into an epic quest when the wizard Gandalf and thirteen dwarves arrive at his door, seeking to reclaim their stolen treasure from the dragon Smaug. Along the way, Bilbo discovers courage he never knew he had and comes into possession of a mysterious ring.',
        9780547928227,
        'Fantasy, Adventure',
        1937,
        'J.R.R. Tolkien',
        'Mariner Books',
        4.6
    ),
    (
        '2a8f5d1c-7b4e-4c9a-8d3f-6e1b9a4c7f2d',
        'The Da Vinci Code',
        'Harvard symbologist Robert Langdon is summoned to the Louvre after the murder of a curator, whose body is found surrounded by cryptic symbols. Teaming up with cryptologist Sophie Neveu, Langdon uncovers a centuries-old conspiracy involving the Holy Grail, secret societies, and hidden messages in Leonardo da Vinci''s masterpieces.',
        9780307474278,
        'Thriller, Mystery',
        2003,
        'Dan Brown',
        'Anchor Books',
        3.9
    ),
    (
        '9d3b7e2f-1c6a-4f8d-8b2e-5c4a9f1d7e3b',
        'The Hunger Games',
        'In the dystopian nation of Panem, sixteen-year-old Katniss Everdeen volunteers to take her younger sister''s place in the annual Hunger Games, a televised fight to the death between tributes from the twelve districts. Her defiance inside the arena ignites a spark of rebellion that threatens to engulf the entire nation.',
        9780439023528,
        'Dystopian, Young Adult',
        2008,
        'Suzanne Collins',
        'Scholastic',
        4.3
    ),
    (
        '6f1e9c4b-3a8d-4b7f-9e2c-1d5a8f3b6e4c',
        'Gone Girl',
        'On their fifth wedding anniversary, Nick Dunne''s wife Amy vanishes under suspicious circumstances, and the mounting evidence points squarely at him. Alternating between Nick''s present-day account and Amy''s diary entries, this psychological thriller delivers one of the most shocking twists in modern crime fiction.',
        9780307588371,
        'Thriller, Mystery',
        2012,
        'Gillian Flynn',
        'Crown Publishing Group',
        4.1
    ),
    (
        'b4d2a8f6-5e9c-4a3d-8f7b-2c6e1a9d4f3b',
        'The Kite Runner',
        'Amir, a privileged boy from Kabul, and Hassan, the son of his father''s servant, grow up inseparable until a single act of cowardice shatters their friendship. Years later, living in America, Amir returns to a war-torn Afghanistan to confront the past and seek the redemption he has long avoided.',
        9781594480003,
        'Historical Fiction, Drama',
        2003,
        'Khaled Hosseini',
        'Riverhead Books',
        4.5
    ),
    (
        '7e3c9f1a-2b6d-4e8a-9c4f-5d2b8a1e7f3c',
        'The Alchemist',
        'Andalusian shepherd boy Santiago follows his recurring dream of treasure hidden near the Egyptian pyramids, leaving behind everything he knows to journey across the desert. Guided by a series of mentors, he learns to listen to his heart and pursue his Personal Legend, in this timeless fable about following one''s dreams.',
        9780062315007,
        'Fiction, Inspirational',
        1988,
        'Paulo Coelho',
        'HarperOne',
        4.2
    ),
    (
        '5a1d7b3f-8c4e-4f2a-8d6b-3e9c1f5a7d2b',
        'The Martian',
        'When a fierce dust storm forces his crew to abandon Mars, astronaut Mark Watney is left behind, presumed dead. Stranded with limited supplies, he must rely on his ingenuity, botany skills, and sharp humor to survive on a hostile planet until a rescue mission can reach him.',
        9780553418026,
        'Science Fiction, Adventure',
        2014,
        'Andy Weir',
        'Broadway Books',
        4.5
    );

    """

    return query


def main():
    _db = _parse_db_connection()
    DB_HOST = _db["host"]
    DB_NAME = _db["name"]
    DB_USER = _db["user"]
    DB_PASSWORD = _db["password"]
    DB_PORT = _db["port"]

    # creating database connection
    conn = mysql.connector.connect(
        host=DB_HOST,
        database=DB_NAME,
        user=DB_USER,
        password=DB_PASSWORD,
        port=DB_PORT,
    )

    # Get a cursor
    cursor = conn.cursor()

    # create book table
    book_table_query = create_book_query()
    cursor.execute(book_table_query)

    sys.stdout.write("Creating Book Table \n")

    # inserting book data
    books_data = insert_books_query()
    cursor.execute(books_data)

    sys.stdout.write("Inserting Book Data \n")

    conn.commit()

    # Closing connection
    cursor.close()
    conn.close()


if __name__ == "__main__":
    main()
