"""
setup_database.py

Creates the 'songs' table and imports song data from dataset.csv
into the MySQL database.

Requirements:
- MySQL Server
- mysql-connector-python
"""

import csv
import mysql.connector
from mysql.connector import Error

# -------------------------------
# Database Configuration
# -------------------------------
DB_CONFIG = {
    "host": "localhost",
    "user": "root",
    "password": "YOUR_MYSQL_PASSWORD",
    "database": "song_db"
}

DATASET_FILE = "dataset.csv"


def create_table(cursor):
    """Create the songs table if it does not already exist."""
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS songs (
            id INT AUTO_INCREMENT PRIMARY KEY,
            title VARCHAR(255),
            artist VARCHAR(255),
            genre VARCHAR(100)
        )
    """)


def import_dataset(cursor):
    """Import songs from the CSV dataset."""

    with open(DATASET_FILE, encoding="latin-1") as file:
        reader = csv.DictReader(file)

        for row in reader:
            cursor.execute(
                """
                INSERT INTO songs (title, artist, genre)
                VALUES (%s, %s, %s)
                """,
                (
                    row["title"],
                    row["artist"],
                    row["genre"]
                )
            )


def main():
    try:
        connection = mysql.connector.connect(**DB_CONFIG)

        if connection.is_connected():
            cursor = connection.cursor()

            create_table(cursor)
            import_dataset(cursor)

            connection.commit()

            print("Database created successfully.")
            print("Song dataset imported successfully.")

    except Error as error:
        print(f"Database Error: {error}")

    finally:
        if "connection" in locals() and connection.is_connected():
            cursor.close()
            connection.close()
            print("Database connection closed.")


if __name__ == "__main__":
    main()