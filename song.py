#Importing modules
import tkinter as tk
from tkinter import ttk, messagebox
import mysql.connector

#MySQL Connection
conn = mysql.connector.connect(
    host="localhost",
    user="root",
    password="12345",
    database="song_db"
)
cursor = conn.cursor()

#App startup
class SongSearchApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Music App")

        width, height = 950, 560
        sw = root.winfo_screenwidth()
        sh = root.winfo_screenheight()
        x = (sw // 2) - (width // 2)
        y = (sh // 2) - (height // 2)
        root.geometry(f"{width}x{height}+{x}+{y}")

        self.root.configure(bg="#121212")

        #Sidebar 
        sidebar = tk.Frame(root, bg="#000000", width=160)
        sidebar.pack(side="left", fill="y")

        tk.Label(sidebar, text="Music", fg="#1DB954", bg="#000000",
                 font=("Segoe UI Semibold", 18)).pack(pady=20)

        #Sidebar buttons
        tk.Button(sidebar, text="🏠  Home",
                  command=self.show_home,
                  bg="#000000", fg="white",
                  activebackground="#1DB954",
                  relief="flat",
                  font=("Segoe UI", 11)).pack(fill="x", pady=8)

        tk.Button(sidebar, text="🔍  Search",
                  command=self.show_search,
                  bg="#000000", fg="white",
                  activebackground="#1DB954",
                  relief="flat",
                  font=("Segoe UI", 11)).pack(fill="x", pady=8)

        #Main container
        self.container = tk.Frame(root, bg="#121212")
        self.container.pack(side="right", fill="both", expand=True)

        self.home_frame = tk.Frame(self.container, bg="#121212")
        self.search_frame = tk.Frame(self.container, bg="#121212")

        self.build_home_page()
        self.build_search_page()

        self.show_home()

    #Home page
    def build_home_page(self):

        tk.Label(self.home_frame, text="All Songs",
                 fg="white", bg="#121212",
                 font=("Segoe UI Semibold", 20)).pack(pady=10)

        self.home_count = tk.Label(self.home_frame, text="",
                                   fg="#B3B3B3", bg="#121212",
                                   font=("Segoe UI", 10))
        self.home_count.pack()

        style = ttk.Style()
        style.theme_use("default")
        style.configure("Treeview",
                        background="#181818",
                        foreground="white",
                        rowheight=28,
                        fieldbackground="#181818",
                        font=("Segoe UI", 10))
        style.configure("Treeview.Heading",
                        background="#1f1f1f",
                        foreground="white",
                        font=("Segoe UI Semibold", 10))
        style.map("Treeview",
                  background=[("selected", "#1DB954")],
                  foreground=[("selected", "black")])

        self.home_tree = ttk.Treeview(self.home_frame,
                                      columns=("id","title","artist","genre"),
                                      show="headings")

        for col, txt, w in [
            ("id","ID",50),
            ("title","Title",300),
            ("artist","Artist",250),
            ("genre","Genre",150)
        ]:
            self.home_tree.heading(col, text=txt)
            self.home_tree.column(col, width=w)

        self.home_tree.pack(fill="both", expand=True, padx=15, pady=10)

    #Search page
    def build_search_page(self):

        tk.Label(self.search_frame, text="Search Songs",
                 fg="white", bg="#121212",
                 font=("Segoe UI Semibold", 20)).pack(pady=10)

        search_box = tk.Frame(self.search_frame, bg="#121212")
        search_box.pack(pady=5)

        tk.Label(search_box, text="Search:",
                 fg="white", bg="#121212",
                 font=("Segoe UI", 11)).grid(row=0, column=0)

        self.search_var = tk.StringVar()
        entry = tk.Entry(search_box, textvariable=self.search_var,
                         width=35, font=("Segoe UI", 11),
                         bg="#181818", fg="white",
                         insertbackground="white", relief="flat")
        entry.grid(row=0, column=1, padx=8)

        def make_btn(text, cmd, col):
            tk.Button(search_box, text=text, command=cmd,
                      bg="#1DB954", fg="black",
                      activebackground="#1ed760",
                      relief="flat",
                      font=("Segoe UI Semibold", 10),
                      width=10).grid(row=0, column=col, padx=5)

        make_btn("Title", self.search_title, 2)
        make_btn("Artist", self.search_artist, 3)
        make_btn("Genre", self.search_genre, 4)

        self.search_count = tk.Label(self.search_frame, text="",
                                     fg="#B3B3B3", bg="#121212",
                                     font=("Segoe UI", 10))
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


        self.search_tree = ttk.Treeview(self.search_frame,
                                        columns=("id","title","artist","genre"),
                                        show="headings")

        for col, txt, w in [
            ("id","ID",60),
            ("title","Title",300),
            ("artist","Artist",250),
            ("genre","Genre",150)
        ]:
            self.search_tree.heading(col, text=txt)
            self.search_tree.column(col, width=w)

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

    #Page switchers
    def show_home(self):
        self.search_frame.pack_forget()
        self.home_frame.pack(fill="both", expand=True)
        self.load_home_songs()

    def show_search(self):
        self.home_frame.pack_forget()
        self.search_frame.pack(fill="both", expand=True)

    #Home data
    def load_home_songs(self):
        self.home_tree.delete(*self.home_tree.get_children())
        cursor.execute("SELECT * FROM songs")
        rows = cursor.fetchall()
        self.home_count.config(text=f"{len(rows)} songs in library")
        for r in rows:
            self.home_tree.insert("", "end", values=r)

    def recommend_from_search(self):
        selected = self.search_tree.focus()
    
        if not selected:
            messagebox.showwarning("No selection", "Select a song from search results")
            return
    
        song = self.search_tree.item(selected)['values']
        song_id, title, artist, genre = song
    
        # same artist first
        cursor.execute("""
            SELECT title, artist, genre FROM songs
            WHERE artist = %s AND id != %s
            LIMIT 10
        """, (artist, song_id))
        recs = cursor.fetchall()
    
        # same genre fallback
        if len(recs) < 5:
            cursor.execute("""
                SELECT title, artist, genre FROM songs
                WHERE genre = %s AND id != %s
                LIMIT 10
            """, (genre, song_id))
            recs += cursor.fetchall()
    
        # popup window
        win = tk.Toplevel(self.root)
        win.title("Recommended Songs")
        win.geometry("600x400")
        win.configure(bg="#121212")
    
        tk.Label(
            win,
            text=f"Because you searched & selected: {title}",
            fg="white",
            bg="#121212",
            font=("Segoe UI Semibold", 12)
        ).pack(pady=10)
    
        t = ttk.Treeview(
            win,
            columns=("Title", "Artist", "Genre"),
            show="headings"
        )
    
        for col, txt, w in [
            ("Title","Title",260),
            ("Artist","Artist",200),
            ("Genre","Genre",120)
        ]:
            t.heading(col, text=txt)
            t.column(col, width=w)
    
        t.pack(fill="both", expand=True, padx=10, pady=10)
    
        if not recs:
            t.insert("", "end", values=("No recommendations found", "", ""))
        else:
            for r in recs:
                t.insert("", "end", values=r)

    #Sinple search
    def run_search(self, query, value):
        self.search_tree.delete(*self.search_tree.get_children())
        cursor.execute(query, (f"%{value}%",))
        rows = cursor.fetchall()
        self.search_count.config(text=f"{len(rows)} songs found")
        for r in rows:
            self.search_tree.insert("", "end", values=r)

    def search_title(self):
        self.run_search("SELECT * FROM songs WHERE title LIKE %s", self.search_var.get())

    def search_artist(self):
        self.run_search("SELECT * FROM songs WHERE artist LIKE %s", self.search_var.get())

    def search_genre(self):
        self.run_search("SELECT * FROM songs WHERE genre LIKE %s", self.search_var.get())

    #Reccomendation system
    def recommend_selected(self):
        selected = self.home_tree.focus()

        if not selected:
            messagebox.showwarning("No selection", "Select a song first")
            return

        song = self.home_tree.item(selected)['values']
        song_id, title, artist, genre = song

        # same artist first
        cursor.execute("""
            SELECT title, artist, genre FROM songs
            WHERE artist = %s AND id != %s
            LIMIT 10
        """, (artist, song_id))
        recs = cursor.fetchall()

        # same genre fallback
        if len(recs) < 5:
            cursor.execute("""
                SELECT title, artist, genre FROM songs
                WHERE genre = %s AND id != %s
                LIMIT 10
            """, (genre, song_id))
            recs += cursor.fetchall()

        # popup window
        win = tk.Toplevel(self.root)
        win.title("Recommended Songs")
        win.geometry("600x400")
        win.configure(bg="#121212")

        tk.Label(win,
                 text=f"Because you listened to: {title}",
                 fg="white",
                 bg="#121212",
                 font=("Segoe UI Semibold", 12)
                 ).pack(pady=10)

        t = ttk.Treeview(win,
                         columns=("Title", "Artist", "Genre"),
                         show="headings")

        for col, txt, w in [
            ("Title","Title",260),
            ("Artist","Artist",200),
            ("Genre","Genre",120)
        ]:
            t.heading(col, text=txt)
            t.column(col, width=w)

        t.pack(fill="both", expand=True, padx=10, pady=10)

        if not recs:
            t.insert("", "end", values=("No recommendations found", "", ""))
        else:
            for r in recs:
                t.insert("", "end", values=r)

    def add_song_window(self):
        win = tk.Toplevel(self.root)
        win.title("Add Song")
        win.geometry("350x300")
        win.configure(bg="#121212")

        fields = ["Title", "Artist", "Genre"]
        entries = {}

        for field in fields:
            tk.Label(win, text=field, fg="white", bg="#121212",
                     font=("Segoe UI", 10)).pack(pady=4)
            e = tk.Entry(win, font=("Segoe UI", 10))
            e.pack(fill="x", padx=20)
            entries[field] = e

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
            win.destroy()
            self.search_genre()  # refresh search results

        tk.Button(
            win,
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

        song = self.search_tree.item(selected)['values']
        song_id, title, artist, genre = song

        win = tk.Toplevel(self.root)
        win.title("Edit Song")
        win.geometry("350x300")
        win.configure(bg="#121212")

        tk.Label(win, text="Title", fg="white", bg="#121212").pack(pady=4)
        title_e = tk.Entry(win)
        title_e.pack(fill="x", padx=20)
        title_e.insert(0, title)

        tk.Label(win, text="Artist", fg="white", bg="#121212").pack(pady=4)
        artist_e = tk.Entry(win)
        artist_e.pack(fill="x", padx=20)
        artist_e.insert(0, artist)

        tk.Label(win, text="Genre", fg="white", bg="#121212").pack(pady=4)
        genre_e = tk.Entry(win)
        genre_e.pack(fill="x", padx=20)
        genre_e.insert(0, genre)

        def update_song():
            cursor.execute(
                "UPDATE songs SET title=%s, artist=%s, genre=%s WHERE id=%s",
                (title_e.get(), artist_e.get(), genre_e.get(), song_id)
            )
            conn.commit()
            win.destroy()
            self.search_genre()  # refresh search results

        tk.Button(
            win,
            text="Update",
            command=update_song,
            bg="#1DB954",
            fg="black",
            relief="flat",
            font=("Segoe UI Semibold", 10)
        ).pack(pady=15)


#Main
root = tk.Tk()
app = SongSearchApp(root)
root.mainloop()

