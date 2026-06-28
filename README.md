Music Recommendation App
## THIS WAS A TEAM PROJECT AND ONLY THE BASIC LOGIC CODE WAS HANDLED BY ME##

A desktop music management application built using Python, Tkinter, and MySQL.
The project focuses on database handling, GUI development, and rule-based recommendation logic.

Purpose

This project helped me strengthen my understanding of:

Python application structure
GUI development using Tkinter
Database integration using MySQL
CRUD operations (Create, Read, Update, Delete)
Basic rule-based recommendation systems
Features
Add new songs to the database
Search songs by name or artist
Edit existing song details
View all stored songs
Recommend similar songs based on:
Artist similarity
Genre matching
How Recommendation Works

The recommendation system uses a rule-based approach:

When a song is selected, the system queries the database for:
Songs by the same artist (highest priority)
Songs with the same genre (secondary priority)
Results are retrieved using SQL queries and displayed in the GUI

Note: This is a rule-based system and does not use machine learning.

-Technologies Used
  Python
  Tkinter (GUI)
  MySQL (Database)
  mysql-connector-python
  Database Structure

-Table: songs

  id (INT, Primary Key)
  title (VARCHAR)
  artist (VARCHAR)
  genre (VARCHAR)

-How to Run
  Install dependencies:
    pip install mysql-connector-python
  Create database:
    CREATE DATABASE song_db;
  Run database setup:
    python set_db.py
  Start application:
    python main.py

