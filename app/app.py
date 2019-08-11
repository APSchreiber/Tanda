import sys, os, bottle, requests, collections

#sys.path = ['/var/www/apschreiber/migrations/'] + sys.path
os.chdir(os.path.dirname(__file__))

import sqlite3, json, nltk
from bottle import *
from bottle import template
from datetime import datetime

############################################

bottle.debug(True)
#bottle.TEMPLATES.clear()

############################################

db_name = 'data/tanda.db'

people_cols = ('eto', 'first', 'last', 'middle', 'suffix', 'email', 'phone', 'dob', 'address', 'description')
people_vw_cols = ('first', 'last', 'middle', 'suffix', 'email', 'phone', 'dob', 'description', 'address1', 'address2', 'city', 'state', 'zip', 'country')

places_cols = ('address1', 'address2', 'city', 'state', 'zip', 'country', 'description', 'comments')
circles_cols = ('name', 'start', 'months', 'loan', 'capacity', 'description', 'comments')

############################################

### View Models ###

class Circle_vm:
  def __init__(self, id, name, start, finish, loan, capacity, enrolled, participants, people_list):
    self.id = id
    self.name = name
    self.start = start
    self.finish = finish
    self.loan = loan
    self.capacity = capacity
    self.enrolled = enrolled
    self.participants = participants
    self.people_list = people_list

class Participant_vm:
  def __init__(self, person_id, person_name, account, circle_name):
    self.person_id = person_id
    self.person_name = person_name
    self.account = account,
    self.circle_name = circle_name

############################################

def check(username, password):
  if username == password:
    return True
  return False

def strip_quotes_list(lst):
  return str(lst).replace("'", "")  
  
def build_sep(col, sep):
  i = 0
  count = len(col)
  lst = ""
  for item in col:
    if i < count - 1:
      lst += item + sep 
    else:
      lst += item
    i += 1
  return lst
    
def build_insert(names, table, data):
  nr = str(names).replace("'", "")
  
  vals = "("
  for n in names:
    vals += "?,"
  vals = vals[:-1] + ")"
  
  sql = "INSERT INTO " + table + " " + nr + " VALUES " + vals
  d = []
  for n in names:
    d.append(data[n])
  return (sql, tuple(d))

def build_update(names, table, data, id):
  sets = ""
  for n in names:
    if data[n] is not None:
      exp = n + " = '" + data[n] + "', "
      sets += exp
  sets = sets[:-2]
  sql = "UPDATE " + table + " SET " + sets + " WHERE id = " + id
  return sql
  
def build_select(names, table, where):
  nr = str(names).replace("'", "")
  sql = "SELECT " + build_sep(names, ", ") + " FROM " + table + " WHERE " + where
  return sql
  
def dict_builder(cols, values):
  i = 0
  d = collections.OrderedDict()
  for c in cols:
    d[c] = values[i]
    i += 1
  return d
  
def response_dict(result, cols):
  response = {}
  response["items"] = []
  for r in result:
    item = dict_builder(cols, r)
    response["items"].append(item)
  return response
############################################

@error(500)
def custom500(error):
  return "Error: " + str(error)

@route('/errors')
def errors():
  return static_file('error.log', root='../logs')

@route('/')
def root_static():
  return static_file('index.html', root='../')

# Static Routes
@get("/static/html/<filepath:re:.*\.html>")
def css(filepath):
    return static_file(filepath, root="../static/css")

@get("/static/css/<filepath:re:.*\.css>")
def css(filepath):
    return static_file(filepath, root="../static/css")

@get("/static/img/<filepath:re:.*\.(jpg|png|gif|ico|svg)>")
def img(filepath):
    return static_file(filepath, root="../static/img")

@get('/static/js/<filepath:path>')
def js(filepath):
  return static_file(filepath, root='../static/js')

@route('/baker')
def manager():
  return static_file('baker.html', root='../static/')

  conn = sqlite3.connect(db_name)
  c = conn.cursor()
  c.execute("SELECT * FROM circles")
  result = c.fetchall()
  c.close()
  response = {}
  response["items"] = []
  for r in result:
    item = dict_builder(("id",) + circles_cols, r)
    response["items"].append(item)

  return template('views/circles', items=response["items"])

#########################
###### Accounts ######
#########################

# Accounts Manager Page
@route('/accounts/manage')
def accounts_manage():
  conn = sqlite3.connect(db_name)
  c = conn.cursor()
  c.execute("SELECT id, person, comments FROM accounts")
  result = c.fetchall()
  c.close()
  response = {}
  response["items"] = []
  for r in result:
    item = dict_builder(("id", "person", "comments"), r)
    response["items"].append(item)

  return template('views/accounts', items=response["items"])

# Return a listing of accounts
@route('/accounts/list/<format>')
def listAccounts(format):

  conn = sqlite3.connect(db_name)
  c = conn.cursor()
  c.execute("SELECT id, person, comments FROM accounts")
  result = c.fetchall()
  c.close()
  response = {}
  response["items"] = []
  for r in result:
    item = dict_builder(("id", "person", "comments"), r)
    response["items"].append(item)
  
  if format == 'table':
    return template('views/item_table', items=response["items"])
  
  return response

  
#########################
###### Circles ######
#########################

@route('/circles/details/<id>')
def circles_details(id):
  conn = sqlite3.connect(db_name)
  c = conn.cursor()

  # get the circle
  c.execute("SELECT id, name, start, finish, loan, capacity, enrolled FROM circles_vw WHERE id = ?", (id,))
  result_circles = c.fetchall()
  circle = result_circles[0]
  
  # get participants in circle
  c.execute("SELECT personid, first, last, payout_order, distribution, circle_balance FROM participants_vw WHERE circleid = ?", (2,))
  result_participants = c.fetchall()

  # get available people
  c.execute("SELECT id, first, last FROM people")
  result_people = c.fetchall()

  conn.close()

  table_participants = {}
  table_participants['heads'] = ("id", "first", "last", "payout_order", "distribution", "circle_balance")
  table_participants['rows'] = []
  for r in result_participants:
    item = dict_builder(table_participants['heads'], r)
    table_participants['rows'].append(item)

  vm = Circle_vm(circle[0], circle[1], circle[2], circle[3], circle[4], circle[5], circle[6], result_participants, result_people)
  tables = [table_participants]

  return template('views/circle', model=vm, tables=tables)


@route('/circles/manage')
def circles_manage():

  conn = sqlite3.connect(db_name)
  c = conn.cursor()
  c.execute("SELECT * FROM circles")
  result = c.fetchall()
  c.close()
  response = {}
  response["items"] = []
  for r in result:
    item = dict_builder(("id",) + circles_cols, r)
    response["items"].append(item)

  return template('views/circles', items=response["items"])


@route('/circles/list/<format>')
def listCircles(format):

  conn = sqlite3.connect(db_name)
  c = conn.cursor()
  c.execute("SELECT * FROM circles")
  result = c.fetchall()
  c.close()
  response = {}
  response["items"] = []
  for r in result:
    item = dict_builder(("id",) + circles_cols, r)
    response["items"].append(item)
  
  if format == 'table':
    return template('views/item_table', items=response["items"])
  
  return response

# Add a new circle
@route('/circles/add', method='POST')
def add_circles():
  data = request.json
  conn = sqlite3.connect(db_name)
  c = conn.cursor()
  sql = build_insert(circles_cols, "circles", request.json)
  c.execute(sql[0], sql[1])
  conn.commit()
  
  return {"success": True}

# Get a circle
@route('/circles/<id>', method='GET')
def circles(id):
  conn = sqlite3.connect(db_name)
  c = conn.cursor()
  c.execute(build_select(circles_cols, 'circles', "id = ?"), (id,))
  result = c.fetchall()
  c.close()
  
  return response_dict(result, circles_cols)
  
# Update circle
@route('/circles/<id>', method='POST')
def edit_circles(id):
  data = request.json
  conn = sqlite3.connect(db_name)
  c = conn.cursor()
  sql = build_update(circles_cols, "circles", data, id)
  c.execute(sql)
  conn.commit()
  
  return {"success": True}

# Remove circle
@route('/circles/r/<id>', method='GET')
@auth_basic(check)
def r_circles(id):
  conn = sqlite3.connect(db_name)
  c = conn.cursor()
  c.execute("DELETE FROM circles WHERE id = ?", (id,))
  conn.commit()
  c.close()
  
  return {"success": True}

# Add a percon to a circle
@route('/circles_people/add/<circleid>/<personid>', method='POST')
def circles_add_people(circleid, personid):
  conn = sqlite3.connect(db_name)
  c = conn.cursor()
  
  # add person to circle
  c.execute("INSERT INTO circles_people (circleid, personid) VALUES (?, ?)", (circleid, personid))

  # add a default payment to the circle for the person
  c.execute("SELECT id, person FROM accounts WHERE person = ?", (personid,))
  account_id = c.fetchone()[0]
  current_date = datetime.now().strftime("%Y-%m-%d")
  sql = "INSERT INTO payments ('person', 'account', 'circle', 'amount', 'date', 'comments') VALUES (?, ?, ?, ?, ?, ?)"
  c.execute(sql, (personid, account_id, circleid, 0, '2019-12-03', 'Initial payment on circle add'))

  conn.commit()
  conn.close()
  return {"success": True}


#########################
###### People ######
#########################

# People Manager Page
@route('/people/manage')
def people_manage():
  conn = sqlite3.connect(db_name)
  c = conn.cursor()
  c.execute("SELECT id, first, last, middle, suffix, email, phone, dob, description, address1, address2, city, state, zip, country FROM people_vw")
  result = c.fetchall()
  c.close()
  response = {}
  response["items"] = []
  for r in result:
    item = dict_builder(("id",) + people_vw_cols, r)
    response["items"].append(item)

  return template('views/people', items=response["items"])

# Return a listing of people
@route('/people/list/<format>')
def listPeople(format):
  conn = sqlite3.connect(db_name)
  c = conn.cursor()
  c.execute("SELECT id, first, last, middle, suffix, email, phone, dob, description, address1, address2, city, state, zip, country FROM people_vw")
  result = c.fetchall()
  c.close()
  response = {}
  response["items"] = []
  for r in result:
    item = dict_builder(("id",) + people_vw_cols, r)
    response["items"].append(item)
  
  if format == 'table':
    return template('views/item_table', items=response["items"])
  
  return response

# Add People
@route('/people/add', method='POST')
def add_people():
  data = request.json
  conn = sqlite3.connect(db_name)
  c = conn.cursor()

  # add the person
  sql = build_insert(people_cols, "people", request.json)
  c.execute(sql[0], sql[1])

  # create an account for the person
  new_person_id = c.lastrowid
  sql = build_insert(('person', 'comments'), 'accounts', json.loads('{"person": ' + str(new_person_id) + ', "comments": "Auto create"}'))
  c.execute(sql[0], sql[1])
  conn.commit()

  # add a defult payment to the account
  new_account_id = c.lastrowid
  current_date = datetime.now().strftime("%m-%d-%Y")
  sql = "INSERT INTO payments ('person', 'account', 'amount', 'date', 'comments') VALUES (?, ?, 0, ?, 'Payment on auto create')"
  c.execute(sql, (new_person_id, new_account_id, current_date))

  c.close()
  
  return {"success": True}

# Get Person
@route('/people/<id>', method='GET')
def people(id):
  conn = sqlite3.connect(db_name)
  c = conn.cursor()
  c.execute(build_select(people_cols, 'people', "id = ?"), (id,))
  result = c.fetchall()
  c.close()
  
  return response_dict(result, people_cols)

# Update Person
@route('/people/<id>', method='POST')
def edit_people(id):
  data = request.json
  conn = sqlite3.connect(db_name)
  c = conn.cursor()
  sql = build_update(people_cols, "people", data, id)
  c.execute(sql)
  conn.commit()
  
  return {"success": True}

# Remove Person
@route('/people/r/<id>', method='GET')
@auth_basic(check)
def r_people(id):
  conn = sqlite3.connect(db_name)
  c = conn.cursor()
  c.execute("DELETE FROM people WHERE id = ?", (id,))
  conn.commit()
  c.close()
  
  return {"success": True}

# Details page for participant in a circle
@route('/circles_people/details/<circleid>/<personid>')
def circles_people_details(circleid, personid):
  conn = sqlite3.connect(db_name)
  c = conn.cursor()
  
  # get person
  c.execute("SELECT circleid, name, personid, first, last, middle, suffix, email, phone, accountid, accountno FROM participants_vw WHERE personid = ?", (personid,))
  person = c.fetchone()

  # get payments for person
  c.execute("SELECT id, date, amount, person, account FROM payments WHERE person = ? AND circle = ?", (personid, circleid))
  payments_result = c.fetchall()
  
  c.close()
  response = {}
  response["items"] = []
  for r in payments_result:
    item = dict_builder(("id", "date", "amount", "person", "account"), r)
    response["items"].append(item)

  vm = Participant_vm(person_id=person[2], person_name=person[3] + " " + person[4], account=person[9], circle_name=person[1])

  return template('views/circles_person', model=vm, items=response["items"])

# Return a listing of people in a circle
@route('/circles_people/list/<format>')
def listCirclesPeople(format):
  conn = sqlite3.connect(db_name)
  c = conn.cursor()
  c.execute("SELECT personid, first, last, payout_order, distribution, circle_balance FROM participants_vw")
  result = c.fetchall()
  c.close()
  response = {}
  response["items"] = []
  for r in result:
    item = dict_builder(("id", "first", "last", "payout_order", "distribution", "circle_balance"), r)
    response["items"].append(item)
  
  if format == 'table':
    return template('views/item_table', items=response["items"])
  
  return response

#########################
###### Payments ######
#########################

# Add payment
@route('/payments/add', method='POST')
def add_payment():
  data = request.json
  conn = sqlite3.connect(db_name)
  c = conn.cursor()

  # add the payment
  sql = build_insert(("date", "amount", "person", "account"), "payments", request.json)
  c.execute(sql[0], sql[1])
  conn.commit()
  
  return {"success": True}

# Return a listing of payments
@route('/payments/list/<format>')
def listPayments(format):
  conn = sqlite3.connect(db_name)
  c = conn.cursor()
  c.execute("SELECT id, date, amount, person, account FROM payments")
  result = c.fetchall()
  c.close()
  response = {}
  response["items"] = []
  for r in result:
    item = dict_builder(("id", "date", "amount", "person", "account"), r)
    response["items"].append(item)
  
  if format == 'table':
    return template('views/item_table', items=response["items"])
  
  return response


#########################
###### Places ######
#########################

# Address Manager Page
@route('/places/manage')
def places_manage():
  conn = sqlite3.connect(db_name)
  c = conn.cursor()
  c.execute("SELECT * FROM places")
  result = c.fetchall()
  c.close()
  response = {}
  response["items"] = []
  for r in result:
    item = dict_builder(("id",) + places_cols, r)
    response["items"].append(item)

  return template('views/places', items=response["items"])

# Return a listing of addresses
@route('/places/list/<format>')
def listPlaces(format):
  conn = sqlite3.connect(db_name)
  c = conn.cursor()
  c.execute("SELECT * FROM places")
  result = c.fetchall()
  c.close()
  response = {}
  response["items"] = []
  for r in result:
    item = dict_builder(("id",) + places_cols, r)
    response["items"].append(item)
  
  if format == 'table':
    return template('views/item_table', items=response["items"])
  
  return response

# Add an address
@route('/places/add', method='POST')
def add_places():
  data = request.json
  conn = sqlite3.connect(db_name)
  c = conn.cursor()
  sql = build_insert(places_cols, "places", request.json)
  c.execute(sql[0], sql[1])
  conn.commit()
  
  return {"success": True}

# Get an address
@route('/places/<id>', method='GET')
def places(id):
  conn = sqlite3.connect(db_name)
  c = conn.cursor()
  c.execute(build_select(places_cols, 'places', "id = ?"), (id,))
  result = c.fetchall()
  c.close()
  
  return response_dict(result, places_cols)
  
# Update an address
@route('/places/<id>', method='POST')
def edit_places(id):
  data = request.json
  conn = sqlite3.connect(db_name)
  c = conn.cursor()
  sql = build_update(places_cols, "places", data, id)
  c.execute(sql)
  conn.commit()
  
  return {"success": True}

# Remove an address
@route('/places/r/<id>', method='GET')
@auth_basic(check)
def r_places(id):
  conn = sqlite3.connect(db_name)
  c = conn.cursor()
  c.execute("DELETE FROM places WHERE id = ?", (id,))
  conn.commit()
  c.close()
  
  return {"success": True}


#########################
###### Other ######
#########################

@route('/autocomplete/people', method='POST')
def autocomplete():
    search = request.forms.get('search')
    conn = sqlite3.connect(db_name)
    c = conn.cursor()
    c.execute("SELECT CAST(id AS TEXT) as id, first FROM people WHERE first LIKE ?", (str(search) + "%",))
    result = c.fetchall()
    c.close()
    response = {}
    response["items"] = []
    for r in result:
      item = dict_builder(("value", "label"), r)
      response["items"].append(item)
    return json.dumps(response['items'])

@route('/autocomplete/places', method='POST')
def autocomplete():
    search = request.forms.get('search')
    conn = sqlite3.connect(db_name)
    c = conn.cursor()
    c.execute("SELECT CAST(id AS TEXT) as id, address1 FROM places WHERE address1 LIKE ?", (str(search) + "%",))
    result = c.fetchall()
    c.close()
    response = {}
    response["items"] = []
    for r in result:
      item = dict_builder(("value", "label"), r)
      response["items"].append(item)
    return json.dumps(response['items'])

@route('/domains/<t>/<f>')
def domains(t, f):
  conn = sqlite3.connect(db_name)
  c = conn.cursor()
  c.execute("SELECT id, " + f + " FROM " + t)
  result = c.fetchall()
  c.close()
  
  response = {}
  response["items"] = []
  for r in result:
    item = {"id": r[0], "val": r[1]}
    response["items"].append(item)
  
  return response

  

############################################
  
application = bottle.default_app()
