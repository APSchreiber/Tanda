import sqlite3

con = sqlite3.connect('tanda.db')

# People
con.execute("CREATE TABLE people (id INTEGER PRIMARY KEY AUTOINCREMENT, eto INTEGER, first TEXT, last TEXT NOT NULL, middle Text, suffix TEXT, email TEXT, phone TEXT, description TEXT, comments TEXT, dob TEXT, address INTEGER, FOREIGN KEY(address) REFERENCES places(id))")
con.execute("INSERT INTO people (last, first) VALUES ('Stuart', 'Emily')")

# Places
con.execute("CREATE TABLE places (id INTEGER PRIMARY KEY AUTOINCREMENT, address1 TEXT, address2 TEXT, city TEXT, state TEXT, zip TEXT, country TEXT, description TEXT, comments TEXT)")
con.execute("INSERT INTO places (address1, city, state, zip, country) VALUES ('12 Ola Ave.', 'St. Louis', 'MO', '63119', 'USA')")

# Circles
con.execute("CREATE TABLE circles (id INTEGER PRIMARY KEY AUTOINCREMENT, name TEXT, start TEXT, months INTEGER, due INTEGER, loan INTEGER, capacity INTEGER, description TEXT, comments TEXT)")
con.execute("INSERT INTO circles (name, start, months, due, loan, capacity) VALUES ('The First Circle', 9/9/19, 12, 15, 1200, 12)")

con.execute("CREATE TABLE circles_people (circleid INTEGER NOT NULL, peopleid INTEGER NOT NULL, payout_order INTEGER, distribution TEXT, PRIMARY KEY(circleid, peopleid))")

# Accounts
con.execute("CREATE TABLE accounts (id INTEGER PRIMARY KEY AUTOINCREMENT, accountno TEXT, comments TEXT, person INTEGER, FOREIGN KEY(person) REFERENCES people(id))")
con.execute("INSERT INTO accounts (accountno, person) VALUES ('12345', 1)")

# Payments
con.execute("CREATE TABLE payments (id INTEGER PRIMARY KEY AUTOINCREMENT, amount INTEGER NOT NULL, date TEXT, person INTEGER, account INTEGER, circle INTEGER, FOREIGN KEY(account) REFERENCES accounts(id))")

# Views
con.execute("CREATE VIEW people_vw AS SELECT people.id, people.first, people.last, people.middle, people.suffix, people.email, people.phone, people.address, people.description, people.dob, strftime('%m/%d/%Y', people.dob) as dob_format, places.address1, places.address2, places.city, places.state, places.zip, places.country, places.description as place_description FROM people INNER JOIN places on places.id = people.address")


con.commit()
