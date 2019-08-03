import sqlite3

con = sqlite3.connect('tanda.db')

# People
con.execute("CREATE TABLE people (id INTEGER PRIMARY KEY AUTOINCREMENT, last TEXT NOT NULL, first TEXT, middle Text, suffix TEXT, email TEXT, phone TEXT, description TEXT, dob TEXT)")
con.execute("INSERT INTO people (last, first) VALUES ('Stuart', 'Emily')")



con.commit()
