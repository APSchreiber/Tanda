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
con.execute("INSERT INTO circles (name, start, months, loan, capacity) VALUES ('The First Circle', '2019-09-19', 12, 1200, 12)")

con.execute("CREATE TABLE circles_people (circleid INTEGER NOT NULL, personid INTEGER NOT NULL, payout_order INTEGER, distribution TEXT, PRIMARY KEY(circleid, personid))")
con.execute("INSERT INTO circles_people (circleid, personid, payout_order, distribution) VALUES (1, 1, 1, 'full')")

con.execute("CREATE TABLE payout_schedules (circle INTEGER NOT NULL, person INTEGER NOT NULL, payout_order integer NOT NULL, PRIMARY KEY (circle, person, payout_order))")

# Accounts
con.execute("CREATE TABLE accounts (id INTEGER PRIMARY KEY AUTOINCREMENT, accountno TEXT, comments TEXT, person INTEGER, FOREIGN KEY(person) REFERENCES people(id))")
con.execute("INSERT INTO accounts (accountno, person) VALUES ('12345', 1)")

# Payments
con.execute("CREATE TABLE payments (id INTEGER PRIMARY KEY AUTOINCREMENT, amount INTEGER NOT NULL, date TEXT, person INTEGER, account INTEGER, circle INTEGER, comments TEXT, FOREIGN KEY(account) REFERENCES accounts(id))")
con.execute("INSERT INTO payments (amount, date, person, account, circle) VALUES (300, '2019-08-06', 1, 1, 1)")

# Views
con.execute("CREATE VIEW people_vw AS SELECT people.id, people.eto, people.first, people.last, people.middle, people.suffix, people.email, people.phone, people.description, people.dob, strftime('%m/%d/%Y', people.dob) as dob_format, people.address, places.address1, places.address2, places.city, places.state, places.zip, places.country, places.description as place_description, accounts.id as accountid, accounts.accountno FROM people INNER JOIN places on places.id = people.address LEFT JOIN accounts ON people.id = accounts.person")

# con.execute("CREATE VIEW participants_vw AS SELECT circles_people.circleid, circles_people.personid, people.first, people.last, people.middle, people.suffix, circles.name, circles.loan FROM circles_people JOIN people on people.id = circles_people.personid JOIN circles on circles.id = circles_people.circleid")

con.execute("CREATE VIEW circles_vw AS SELECT circles.id, circles.name, (date(circles.start)) as start, (date(circles.start, '+' || circles.months || ' month')) as finish, circles.loan, circles.capacity, COUNT(circles_people.personid) as enrolled FROM circles LEFT JOIN circles_people on circles.id = circles_people.circleid GROUP BY circles.id")
#con.execute("CREATE VIEW circles_vw AS SELECT circles.id, circles.name, (date(circles.start)) as start, (date(circles.start, '+' || circles.months || ' month')) as finish, circles.loan, circles.capacity, COUNT(circles_people.personid) as enrolled FROM circles LEFT JOIN circles_people on circles.id = circles_people.circleid UNION SELECT circles.id, circles.name, (date(circles.start)) as start, (date(circles.start, '+' || circles.months || ' month')) as finish, circles.loan, circles.capacity, COUNT(circles_people.personid) as enrolled FROM circles_people LEFT JOIN circles on circles.id = circles_people.circleid GROUP BY circles.id")

con.execute("CREATE VIEW accounts_vw AS SELECT accounts.id, accounts.accountno, COUNT(payments.id) as payments, SUM(payments.amount) as balance FROM payments JOIN accounts on payments.account = accounts.id GROUP BY accounts.id")

#con.execute("CREATE VIEW participants_vw AS SELECT circles_people.circleid, circles_people.personid, people_vw.eto, people_vw.first, people_vw.last, people_vw.middle, people_vw.suffix, people_vw.email, people_vw.phone, people_vw.dob, circles_vw.name, circles_vw.start, circles_vw.finish, circles_vw.capacity, circles_vw.enrolled, circles_people.payout_order, circles_people.distribution, s1.circle_balance, accounts.id as accountid, accounts.accountno FROM payments JOIN circles_vw ON payments.circle = circles_vw.id JOIN circles_people ON circles_vw.id = circles_people.circleid JOIN people_vw ON circles_people.personid = people_vw.id JOIN accounts ON people_vw.id = accounts.person LEFT JOIN (SELECT payments.account as act, SUM(payments.amount) as circle_balance FROM payments GROUP BY payments.account, payments.circle) s1 ON people_vw.accountid = s1.act GROUP BY people_vw.id")
#con.execute("CREATE VIEW participants_vw AS SELECT circles_people.circleid, circles_people.personid, people_vw.eto, people_vw.first, people_vw.last, people_vw.middle, people_vw.suffix, people_vw.email, people_vw.phone, people_vw.dob, circles_vw.name, circles_vw.start, circles_vw.finish, circles_vw.capacity, circles_vw.enrolled, circles_people.payout_order, circles_people.distribution, s1.circle_balance, accounts.id as accountid, accounts.accountno FROM payments JOIN circles_vw ON payments.circle = circles_vw.id JOIN circles_people ON circles_vw.id = circles_people.circleid JOIN people_vw ON circles_people.personid = people_vw.id JOIN accounts ON people_vw.id = accounts.person LEFT JOIN (SELECT payments.account as act, SUM(payments.amount) as circle_balance FROM payments GROUP BY payments.account, payments.circle) s1 ON people_vw.accountid = s1.act GROUP BY circles_vw.id")
con.execute("CREATE VIEW participants_vw AS SELECT people_vw.eto, people_vw.first, people_vw.last, people_vw.middle, people_vw.suffix, people_vw.email, people_vw.phone, people_vw.dob, people_vw.accountid, people_vw.accountno, circles_people.circleid, circles_people.personid, circles_people.payout_order, circles_people.distribution, circles_vw.name, circles_vw.start, circles_vw.finish, circles_vw.capacity, circles_vw.enrolled, circles_vw.loan, p.circle_balance, p.payments_total, p.payouts_total, p.num_payments, p.num_payouts FROM people_vw JOIN circles_people on people_vw.id = circles_people.personid JOIN circles_vw on circles_people.circleid = circles_vw.id JOIN ( SELECT payments.account as act, payments.circle, SUM(payments.amount) as circle_balance, SUM( CASE WHEN payments.amount > 0 THEN payments.amount ELSE 0 END ) as payments_total, SUM( CASE WHEN payments.amount < 0 THEN payments.amount ELSE 0 END ) as payouts_total, COUNT( CASE WHEN payments.amount > 0 THEN 1 ELSE NULL END ) as num_payments, COUNT( CASE WHEN payments.amount < 0 THEN 1 ELSE NULL END ) as num_payouts, payments.account || '.' || payments.circle as account_circle FROM payments GROUP BY payments.account, payments.circle ) as p ON p.account_circle = people_vw.accountid || '.' || circles_vw.id GROUP BY people_vw.id, circles_vw.id")

con.execute("CREATE VIEW payout_schedules_vw AS SELECT participants_vw.personid, participants_vw.first, participants_vw.last, participants_vw.name, participants_vw.circleid, participants_vw.capacity, participants_vw.enrolled, participants_vw.loan, payout_schedules.payout_order, (participants_vw.loan / participants_vw.capacity) as payment_amount, (participants_vw.loan) as payout_amount , p1.split_num FROM payout_schedules LEFT JOIN participants_vw ON participants_vw.personid = payout_schedules.person AND participants_vw.circleid = payout_schedules.circle JOIN (SELECT payout_schedules.person as p, payout_schedules.circle as c, payout_schedules.payout_order as po, COUNT(*) AS split_num FROM payout_schedules GROUP BY payout_schedules.person, payout_schedules.circle) as p1 ON participants_vw.personid = p1.p AND participants_vw.circleid = p1.c AND payout_schedules.payout_order = p1.po")

con.commit()