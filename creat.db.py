import sqlite3

connection = sqlite3.connect('quiz.db')
cursor = connection.cursor()

cursor.execute('''
CREATE TABLE IF NOT EXISTS categories (
               id INTEGER PRIMARY KEY AUTOINCREMENT,
               name TEXT NOT NULL UNIQUE
               )
''')

cursor.execute('''
CREATE TABLE IF NOT EXISTS questions (
               id INTEGER PRIMARY KEY AUTOINCREMENT,
               category TEXT NOT NULL,
               question TEXT NOT NULL,
               answer TEXT NOT NULL,
               FOREIGN KEY (category) REFERENCES categories(name)
               )
''')

cursor.execute('''
CREATE TABLE IF NOT EXISTS users (
               id INTEGER PRIMARY KEY AUTOINCREMENT,
               username TEXT NOT NULL UNIQUE,
               password TEXT NOT NULL,
               email TEXT NOT NULL UNIQUE,
               first_name TEXT,
               last_name TEXT,
               age INTEGER,
               quiz_results REAL,
               login BOOL NOT NULL DEFAULT 0,
               admin BOOL NOT NULL DEFAULT 0
               )
''')

cursor.execute("INSERT INTO users (username, password, email, first_name, last_name, admin) VALUES (?, ?, ?, ?, ?, ?)",
               ('admin', 'admin', 'admin.admin@gmail.com', 'adminkhan', 'adminian', 1))
cursor.execute("INSERT INTO users (username, password, email, first_name, last_name, admin, quiz_results) VALUES (?, ?, ?, ?, ?, ?, ?)",
               ('user3', 'password3', 'useremail3@gmail.com', 'userfirstname3', 'userlastname3', 0, '10, 9, 8, 7, 10, 4'))

cursor.execute("PRAGMA foreign_keys = ON")
cursor.execute("INSERT INTO categories (name) VALUES (?)", ('Math',))
cursor.execute("INSERT INTO categories (name) VALUES (?)", ('Geography',))
cursor.execute("INSERT INTO categories (name) VALUES (?)", ('Literature',))

cursor.execute("INSERT INTO questions (category, question, answer) VALUES (?, ?, ?)", ('Math', '2+2', '4'))
cursor.execute("INSERT INTO questions (category, question, answer) VALUES (?, ?, ?)", ('Math', '3+4', '7'))
cursor.execute("INSERT INTO questions (category, question, answer) VALUES (?, ?, ?)", ('Math', '10x10', '100'))
cursor.execute("INSERT INTO questions (category, question, answer) VALUES (?, ?, ?)", ('Math', '10/5', '2'))
cursor.execute("INSERT INTO questions (category, question, answer) VALUES (?, ?, ?)", ('Geography', 'Capital of France?', 'Paris'))
cursor.execute("INSERT INTO questions (category, question, answer) VALUES (?, ?, ?)", ('Geography', 'Capital of England?', 'London'))
cursor.execute("INSERT INTO questions (category, question, answer) VALUES (?, ?, ?)", ('Literature', 'Author of Hamlet?', 'Shakespeare'))

connection.commit()
connection.close()