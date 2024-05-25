import sqlite3

conn = sqlite3.connect('database.db')
cursor = conn.cursor()

cursor.execute('''
CREATE TABLE IF NOT EXISTS lb_prodution (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    product TEXT,
    quantity NUMERIC,
    is_type BOOLEAN,
    type TEXT,
    year INTEGER NOT NULL
);
''')

cursor.execute('''
CREATE TABLE IF NOT EXISTS lb_processing (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    cultive TEXT,
    is_type BOOLEAN,
    type TEXT,
    classification TEXT,
    year INTEGER NOT NULL
);
''')

cursor.execute('''
CREATE TABLE IF NOT EXISTS lb_comercialization (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    product TEXT,
    quantity NUMERIC,
    is_type BOOLEAN,
    year INTEGER NOT NULL
);
''')

cursor.execute('''
CREATE TABLE IF NOT EXISTS lb_importation (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    country TEXT,
    quantity NUMERIC,
    value NUMERIC,
    classification TEXT,
    year INTEGER NOT NULL
);
''')

cursor.execute('''
CREATE TABLE IF NOT EXISTS lb_exportation (
    country TEXT,
    quantity NUMERIC,
    value NUMERIC,
    classification TEXT,
    year INTEGER NOT NULL
);
''')

cursor.execute('''
CREATE TABLE IF NOT EXISTS lb_users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    email TEXT NOT NULL UNIQUE,
    name TEXT NOT NULL,
    password TEXT NOT NULL
);
''')

conn.commit()

conn.close()
