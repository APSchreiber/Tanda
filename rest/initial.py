import sqlite3

con = sqlite3.connect('tanda.db')

# People
con.execute("CREATE TABLE people (id INTEGER PRIMARY KEY AUTOINCREMENT, eto INTEGER, first TEXT, last TEXT NOT NULL, middle Text, suffix TEXT, email TEXT, phone TEXT, description TEXT, comments TEXT, dob TEXT, address INTEGER, FOREIGN KEY(address) REFERENCES places(id))")
con.execute("INSERT INTO people (last, first, address) VALUES ('Stuart', 'Emily', 1)")

# Places
con.execute("CREATE TABLE places (id INTEGER PRIMARY KEY AUTOINCREMENT, address1 TEXT, address2 TEXT, city TEXT, state TEXT, zip TEXT, country TEXT, description TEXT, comments TEXT)")
con.execute("INSERT INTO places (address1, city, state, zip, country) VALUES ('12 Ola Ave.', 'St. Louis', 'MO', '63119', 'USA')")

# Circles
con.execute("CREATE TABLE circles (id INTEGER PRIMARY KEY AUTOINCREMENT, name TEXT, start TEXT, months INTEGER, loan INTEGER, capacity INTEGER, description TEXT, comments TEXT)")
con.execute("INSERT INTO circles (name, start, months, loan, capacity) VALUES ('The First Circle', 2019-09-19, 12, 1200, 12)")

con.execute("CREATE TABLE circles_people (circleid INTEGER NOT NULL, peopleid INTEGER NOT NULL, payout_order INTEGER, distribution TEXT, PRIMARY KEY(circleid, peopleid))")
con.execute("INSERT INTO circles_people (circleid, peopleid, payout_order, distribution) VALUES (1, 1, 1, 'full')")

# Accounts
con.execute("CREATE TABLE accounts (id INTEGER PRIMARY KEY AUTOINCREMENT, accountno TEXT, comments TEXT, person INTEGER, FOREIGN KEY(person) REFERENCES people(id))")
con.execute("INSERT INTO accounts (accountno, person) VALUES ('12345', 1)")

# Payments
con.execute("CREATE TABLE payments (id INTEGER PRIMARY KEY AUTOINCREMENT, amount INTEGER NOT NULL, date TEXT, person INTEGER, account INTEGER, circle INTEGER, FOREIGN KEY(account) REFERENCES accounts(id))")
con.execute("INSERT INTO payments (amount, date, person, account, circle) VALUES (300, '2019-08-06', 1, 1, 1)")

# Views
con.execute("CREATE VIEW people_vw AS SELECT people.id, people.eto, people.first, people.last, people.middle, people.suffix, people.email, people.phone, people.description, people.dob, strftime('%m/%d/%Y', people.dob) as dob_format, people.address, places.address1, places.address2, places.city, places.state, places.zip, places.country, places.description as place_description FROM people INNER JOIN places on places.id = people.address")

# con.execute("CREATE VIEW participants_vw AS SELECT circles_people.circleid, circles_people.peopleid, people.first, people.last, people.middle, people.suffix, circles.name, circles.loan FROM circles_people JOIN people on people.id = circles_people.peopleid JOIN circles on circles.id = circles_people.circleid")

con.execute("CREATE VIEW circles_vw AS SELECT circles.id, circles.name, (date(circles.start)) as start, (date(circles.start, '+' || circles.months || ' month')) as finish, circles.loan, circles.capacity, COUNT(circles_people.peopleid) as enrolled FROM circles_people LEFT JOIN circles on circles.id = circles_people.circleid GROUP BY circles.id")

con.execute("CREATE VIEW accounts_vw AS SELECT accounts.id, accounts.accountno, COUNT(payments.id) as payments, SUM(payments.amount) as balance FROM payments JOIN accounts on payments.account = accounts.id GROUP BY accounts.id")

con.execute("CREATE VIEW participants_vw AS SELECT circles_people.circleid, circles_people.peopleid, people_vw.eto, people_vw.first, people_vw.last, people_vw.middle, people_vw.suffix,  people_vw.email, people_vw.phone, people_vw.dob, circles_vw.name, circles_vw.start, circles_vw.finish, circles_vw.capacity, circles_vw.enrolled, circles_people.payout_order, circles_people.distribution, SUM(payments.amount) as circle_balance FROM payments JOIN circles_vw ON payments.circle = circles_vw.id JOIN circles_people ON circles_vw.id = circles_people.circleid JOIN people_vw ON circles_people.peopleid = people_vw.id JOIN accounts ON people_vw.id = accounts.person")

con.commit()
