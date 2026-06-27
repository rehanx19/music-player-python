import csv
import mysql.connector

# connect to mysql
conn = mysql.connector.connect(
    host="localhost",
    user="root",
    password="12345",
    database="song_db"
)

cursor = conn.cursor()

# create table
cursor.execute("""
CREATE TABLE IF NOT EXISTS songs (
    id INT AUTO_INCREMENT PRIMARY KEY,
    title VARCHAR(255),
    artist VARCHAR(255),
    genre VARCHAR(100)
)
""")

# open csv
with open("C:\\Users\\Joshua Ean Paul U\\Downloads\\dataset.csv", encoding="latin-1") as f:
    reader = csv.DictReader(f)

    for row in reader:
        cursor.execute(
            "INSERT INTO songs (title, artist, genre) VALUES (%s, %s, %s)",
            (row["title"], row["artist"], row["genre"])
        )

# save and close
conn.commit()
conn.close()

print("Inserted everything successfully 😄🎵")
