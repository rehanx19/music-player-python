# Import modules
import tkinter as tk
from tkinter import ttk, messagebox
import mysql.connector

# Connect to MySQL
conn = mysql.connector.connect(
    host="localhost",
    user="root",
    password="YOUR_MYSQL_PASSWORD",
    database="song_db"
)
cursor = conn.cursor()


class SongSearchApp:

    def __init__(self, root):
        self.root = root
        self.root.title("Music Recommendation App")

        # Center the window
        width = 950
        height = 560

        screen_width = root.winfo_screenwidth()
        screen_height = root.winfo_screenheight()

        x = (screen_width - width) // 2
        y = (screen_height - height) // 2

        self.root.geometry(f"{width}x{height}+{x}+{y}")
        self.root.configure(bg="#121212")

        # Sidebar
        sidebar = tk.Frame(self.root, bg="#000000", width=160)
        sidebar.pack(side="left", fill="y")

        tk.Label(
            sidebar,
            text="Music",
            fg="#1DB954",
            bg="#000000",
            font=("Segoe UI Semibold", 18)
        ).pack(pady=20)

        tk.Button(
            sidebar,
            text="🏠 Home",
            command=self.show_home,
            bg="#000000",
            fg="white",
            activebackground="#1DB954",
            relief="flat",
            font=("Segoe UI", 11)
        ).pack(fill="x", pady=8)

        tk.Button(
            sidebar,
            text="🔍 Search",
            command=self.show_search,
            bg="#000000",
            fg="white",
            activebackground="#1DB954",
            relief="flat",
            font=("Segoe UI", 11)
        ).pack(fill="x", pady=8)

        # Main content
        self.container = tk.Frame(self.root, bg="#121212")
        self.container.pack(side="right", fill="both", expand=True)

        self.home_frame = tk.Frame(self.container, bg="#121212")
        self.search_frame = tk.Frame(self.container, bg="#121212")

        self.build_home_page()
        self.build_search_page()

        self.show_home()

    def build_home_page(self):

        tk.Label(
            self.home_frame,
            text="All Songs",
            fg="white",
            bg="#121212",
            font=("Segoe UI Semibold", 20)
        ).pack(pady=10)

        self.home_count = tk.Label(
            self.home_frame,
            text="",
            fg="#B3B3B3",
            bg="#121212",
            font=("Segoe UI", 10)
        )
        self.home_count.pack()

        style = ttk.Style()
        style.theme_use("default")

        style.configure(
            "Treeview",
            background="#181818",
            foreground="white",
            fieldbackground="#181818",
            rowheight=28,
            font=("Segoe UI", 10)
        )

        style.configure(
            "Treeview.Heading",
            background="#1F1F1F",
            foreground="white",
            font=("Segoe UI Semibold", 10)
        )

        style.map(
            "Treeview",
            background=[("selected", "#1DB954")],
            foreground=[("selected", "black")]
        )

        self.home_tree = ttk.Treeview(
            self.home_frame,
            columns=("id", "title", "artist", "genre"),
            show="headings"
        )

        columns = [
            ("id", "ID", 50),
            ("title", "Title", 300),
            ("artist", "Artist", 250),
            ("genre", "Genre", 150)
        ]

        for column, heading, width in columns:
            self.home_tree.heading(column, text=heading)
            self.home_tree.column(column, width=width)

        self.home_tree.pack(fill="both", expand=True, padx=15, pady=10)
       def build_search_page(self):

        tk.Label(
            self.search_frame,
            text="Search Songs",
            fg="white",
            bg="#121212",
            font=("Segoe UI Semibold", 20)
        ).pack(pady=10)

        search_box = tk.Frame(self.search_frame, bg="#121212")
        search_box.pack(pady=5)

        tk.Label(
            search_box,
            text="Search:",
            fg="white",
            bg="#121212",
            font=("Segoe UI", 11)
        ).grid(row=0, column=0)

        self.search_var = tk.StringVar()

        entry = tk.Entry(
            search_box,
            textvariable=self.search_var,
            width=35,
            font=("Segoe UI", 11),
            bg="#181818",
            fg="white",
            insertbackground="white",
            relief="flat"
        )
        entry.grid(row=0, column=1, padx=8)

        # Search buttons
        def create_button(text, command, column):
            tk.Button(
                search_box,
                text=text,
                command=command,
                bg="#1DB954",
                fg="black",
                activebackground="#1ED760",
                relief="flat",
                font=("Segoe UI Semibold", 10),
                width=10
            ).grid(row=0, column=column, padx=5)

        create_button("Title", self.search_title, 2)
        create_button("Artist", self.search_artist, 3)
        create_button("Genre", self.search_genre, 4)

        self.search_count = tk.Label(
            self.search_frame,
            text="",
            fg="#B3B3B3",
            bg="#121212",
            font=("Segoe UI", 10)
        )
        self.search_count.pack()

        tk.Button(
            self.search_frame,
            text="🎧 Recommend Similar Songs",
            command=self.recommend_from_search,
            bg="#1DB954",
            fg="black",
            relief="flat",
            font=("Segoe UI Semibold", 10)
        ).pack(pady=6)

        self.search_tree = ttk.Treeview(
            self.search_frame,
            columns=("id", "title", "artist", "genre"),
            show="headings"
        )

        columns = [
            ("id", "ID", 60),
            ("title", "Title", 300),
            ("artist", "Artist", 250),
            ("genre", "Genre", 150)
        ]

        for column, heading, width in columns:
            self.search_tree.heading(column, text=heading)
            self.search_tree.column(column, width=width)

        self.search_tree.pack(fill="both", expand=True, padx=15, pady=10)

        tk.Button(
            self.search_frame,
            text="➕ Add Song",
            command=self.add_song_window,
            bg="#1DB954",
            fg="black",
            relief="flat",
            font=("Segoe UI Semibold", 10)
        ).pack(pady=6)

        self.search_tree.bind("<Double-1>", self.edit_selected_song)

    def show_home(self):
        self.search_frame.pack_forget()
        self.home_frame.pack(fill="both", expand=True)
        self.load_home_songs()

    def show_search(self):
        self.home_frame.pack_forget()
        self.search_frame.pack(fill="both", expand=True)

    def load_home_songs(self):
        self.home_tree.delete(*self.home_tree.get_children())

        cursor.execute("SELECT * FROM songs")
        songs = cursor.fetchall()

        self.home_count.config(text=f"{len(songs)} songs in library")

        for song in songs:
            self.home_tree.insert("", "end", values=song)

    def recommend_from_search(self):

        selected = self.search_tree.focus()

        if not selected:
            messagebox.showwarning(
                "No Selection",
                "Please select a song first."
            )
            return

        song = self.search_tree.item(selected)["values"]
        song_id, title, artist, genre = song
                # Find songs by the same artist
        cursor.execute("""
            SELECT title, artist, genre
            FROM songs
            WHERE artist = %s AND id != %s
            LIMIT 10
        """, (artist, song_id))

        recommendations = cursor.fetchall()

        # If there aren't enough results, recommend songs from the same genre
        if len(recommendations) < 5:
            cursor.execute("""
                SELECT title, artist, genre
                FROM songs
                WHERE genre = %s AND id != %s
                LIMIT 10
            """, (genre, song_id))

            recommendations.extend(cursor.fetchall())

        # Recommendation window
        window = tk.Toplevel(self.root)
        window.title("Recommended Songs")
        window.geometry("600x400")
        window.configure(bg="#121212")

        tk.Label(
            window,
            text=f"Recommendations based on: {title}",
            fg="white",
            bg="#121212",
            font=("Segoe UI Semibold", 12)
        ).pack(pady=10)

        tree = ttk.Treeview(
            window,
            columns=("Title", "Artist", "Genre"),
            show="headings"
        )

        columns = [
            ("Title", "Title", 260),
            ("Artist", "Artist", 200),
            ("Genre", "Genre", 120)
        ]

        for column, heading, width in columns:
            tree.heading(column, text=heading)
            tree.column(column, width=width)

        tree.pack(fill="both", expand=True, padx=10, pady=10)

        if recommendations:
            for song in recommendations:
                tree.insert("", "end", values=song)
        else:
            tree.insert("", "end", values=("No recommendations found", "", ""))
        def run_search(self, query, value):
        self.search_tree.delete(*self.search_tree.get_children())

        cursor.execute(query, (f"%{value}%",))
        songs = cursor.fetchall()

        self.search_count.config(text=f"{len(songs)} songs found")

        for song in songs:
            self.search_tree.insert("", "end", values=song)

    def search_title(self):
        self.run_search(
            "SELECT * FROM songs WHERE title LIKE %s",
            self.search_var.get()
        )

    def search_artist(self):
        self.run_search(
            "SELECT * FROM songs WHERE artist LIKE %s",
            self.search_var.get()
        )

    def search_genre(self):
        self.run_search(
            "SELECT * FROM songs WHERE genre LIKE %s",
            self.search_var.get()
        )

    def recommend_selected(self):

        selected = self.home_tree.focus()

        if not selected:
            messagebox.showwarning(
                "No Selection",
                "Please select a song first."
            )
            return

        song = self.home_tree.item(selected)["values"]
        song_id, title, artist, genre = song

        # Songs by the same artist
        cursor.execute("""
            SELECT title, artist, genre
            FROM songs
            WHERE artist = %s AND id != %s
            LIMIT 10
        """, (artist, song_id))

        recommendations = cursor.fetchall()

        # If there aren't enough results, use the same genre
        if len(recommendations) < 5:
            cursor.execute("""
                SELECT title, artist, genre
                FROM songs
                WHERE genre = %s AND id != %s
                LIMIT 10
            """, (genre, song_id))

            recommendations.extend(cursor.fetchall())

        window = tk.Toplevel(self.root)
        window.title("Recommended Songs")
        window.geometry("600x400")
        window.configure(bg="#121212")

        tk.Label(
            window,
            text=f"Recommendations based on: {title}",
            fg="white",
            bg="#121212",
            font=("Segoe UI Semibold", 12)
        ).pack(pady=10)

        tree = ttk.Treeview(
            window,
            columns=("Title", "Artist", "Genre"),
            show="headings"
        )

        columns = [
            ("Title", "Title", 260),
            ("Artist", "Artist", 200),
            ("Genre", "Genre", 120)
        ]

        for column, heading, width in columns:
            tree.heading(column, text=heading)
            tree.column(column, width=width)

        tree.pack(fill="both", expand=True, padx=10, pady=10)

        if recommendations:
            for song in recommendations:
                tree.insert("", "end", values=song)
        else:
            tree.insert("", "end", values=("No recommendations found", "", ""))

    def add_song_window(self):

        window = tk.Toplevel(self.root)
        window.title("Add Song")
        window.geometry("350x300")
        window.configure(bg="#121212")

        fields = ["Title", "Artist", "Genre"]
        entries = {}

        for field in fields:
            tk.Label(
                window,
                text=field,
                fg="white",
                bg="#121212",
                font=("Segoe UI", 10)
            ).pack(pady=4)

            entry = tk.Entry(window, font=("Segoe UI", 10))
            entry.pack(fill="x", padx=20)

            entries[field] = entry

        def save_song():

            title = entries["Title"].get()
            artist = entries["Artist"].get()
            genre = entries["Genre"].get()

            if not title or not artist or not genre:
                return

            cursor.execute(
                "INSERT INTO songs (title, artist, genre) VALUES (%s, %s, %s)",
                (title, artist, genre)
            )

            conn.commit()

            window.destroy()
            self.search_genre()

        tk.Button(
            window,
            text="Save",
            command=save_song,
            bg="#1DB954",
            fg="black",
            relief="flat",
            font=("Segoe UI Semibold", 10)
        ).pack(pady=15)

    def edit_selected_song(self, event):

        selected = self.search_tree.focus()

        if not selected:
            return

        song = self.search_tree.item(selected)["values"]
        song_id, title, artist, genre = song

        window = tk.Toplevel(self.root)
        window.title("Edit Song")
        window.geometry("350x300")
        window.configure(bg="#121212")

        tk.Label(window, text="Title", fg="white", bg="#121212").pack(pady=4)
        title_entry = tk.Entry(window)
        title_entry.pack(fill="x", padx=20)
        title_entry.insert(0, title)

        tk.Label(window, text="Artist", fg="white", bg="#121212").pack(pady=4)
        artist_entry = tk.Entry(window)
        artist_entry.pack(fill="x", padx=20)
        artist_entry.insert(0, artist)

        tk.Label(window, text="Genre", fg="white", bg="#121212").pack(pady=4)
        genre_entry = tk.Entry(window)
        genre_entry.pack(fill="x", padx=20)
        genre_entry.insert(0, genre)

        def update_song():

            cursor.execute(
                "UPDATE songs SET title=%s, artist=%s, genre=%s WHERE id=%s",
                (
                    title_entry.get(),
                    artist_entry.get(),
                    genre_entry.get(),
                    song_id
                )
            )

            conn.commit()

            window.destroy()
            self.search_genre()

        tk.Button(
            window,
            text="Update",
            command=update_song,
            bg="#1DB954",
            fg="black",
            relief="flat",
            font=("Segoe UI Semibold", 10)
        ).pack(pady=15)


root = tk.Tk()
app = SongSearchApp(root)
root.mainloop()