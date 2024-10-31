import sqlite3

# Connect to the database (creates tilavaraus.db if it doesn’t exist)
connection = sqlite3.connect('tilavaraus.db')
cursor = connection.cursor()

# Create the tables
cursor.execute('''
    CREATE TABLE IF NOT EXISTS tilat (
        id INTEGER PRIMARY KEY,
        tilan_nimi TEXT NOT NULL
    )
''')

cursor.execute('''
    CREATE TABLE IF NOT EXISTS varaajat (
        id INTEGER PRIMARY KEY,
        nimi TEXT NOT NULL
    )
''')

cursor.execute('''
    CREATE TABLE IF NOT EXISTS varaukset (
        id INTEGER PRIMARY KEY,
        tila INTEGER NOT NULL,
        varaaja INTEGER NOT NULL,
        varauspaiva TEXT NOT NULL,
        FOREIGN KEY (tila) REFERENCES tilat(id),
        FOREIGN KEY (varaaja) REFERENCES varaajat(id)
    )
''')

# Commit changes and close the connection
connection.commit()
connection.close()
