import sys, os, bottle, requests, collections

#sys.path = ['/var/www/apschreiber/migrations/'] + sys.path
os.chdir(os.path.dirname(__file__))

import sqlite3, json, nltk
from bottle import *
from bottle import template


############################################

bottle.debug(True)
#bottle.TEMPLATES.clear()

############################################

db_name = 'tanda.db'

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

@route('/')
def root_static():
  return static_file('index.html', root='../')
    
@route('/static/<filepath:path>')
def serve_static(filepath):
  return static_file(filepath, root='../')

@route('/baker')
def root_static():
  return static_file('baker.html', root='../baker/')


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

  return template('tpl/accounts', items=response["items"])

# Return a listing of accounts
@route('/list_accounts/<format>')
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
    return template('tpl/item_table', items=response["items"])
  
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
  c.execute("SELECT circleid, first, last FROM participants_vw WHERE circleid = ?", (id,))
  result_participants = c.fetchall()

  # get available people
  c.execute("SELECT id, first, last FROM people")
  result_people = c.fetchall()

  conn.close()

  bag_participants = {}
  bag_participants["items"] = []
  for r in result_participants:
    item = dict_builder(("circleid", "first", "last"), r)
    bag_participants["items"].append(item)

  vm = Circle_vm(circle[0], circle[1], circle[2], circle[3], circle[4], circle[5], circle[6], result_participants, result_people)

  return template('tpl/circle', model=vm, items=bag_participants["items"])


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

  return template('tpl/circles', items=response["items"])


@route('/list_circles/<format>')
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
    return template('tpl/item_table', items=response["items"])
  
  return response

@route('/add_circles', method='POST')
def add_circles():
  data = request.json
  conn = sqlite3.connect(db_name)
  c = conn.cursor()
  sql = build_insert(circles_cols, "circles", request.json)
  c.execute(sql[0], sql[1])
  conn.commit()
  
  return {"success": True}


@route('/circles/<id>', method='GET')
def circles(id):
  conn = sqlite3.connect(db_name)
  c = conn.cursor()
  c.execute(build_select(circles_cols, 'circles', "id = ?"), (id,))
  result = c.fetchall()
  c.close()
  
  return response_dict(result, circles_cols)
  
@route('/circles/<id>', method='POST')
def edit_circles(id):
  data = request.json
  conn = sqlite3.connect(db_name)
  c = conn.cursor()
  sql = build_update(circles_cols, "circles", data, id)
  c.execute(sql)
  conn.commit()
  
  return {"success": True}


@route('/r_circles/<id>', method='GET')
@auth_basic(check)
def r_circles(id):
  conn = sqlite3.connect(db_name)
  c = conn.cursor()
  c.execute("DELETE FROM circles WHERE id = ?", (id,))
  conn.commit()
  c.close()
  
  return {"success": True}


@route('/circles/addperson/<id>/<personid>')
def circles_add_people(id, personid):
  conn = sqlite3.connect(db_name)
  c = conn.cursor()
  c.execute("INSERT INTO circles_people (circleid, peopleid) VALUES (?, ?)", (id, personid))
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

  return template('tpl/people', items=response["items"])

# Return a listing of people
@route('/list_people/<format>')
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
    return template('tpl/item_table', items=response["items"])
  
  return response

# Add People
@route('/add_people', method='POST')
def add_people():
  data = request.json
  conn = sqlite3.connect(db_name)
  c = conn.cursor()

  # add the person
  sql = build_insert(people_cols, "people", request.json)
  c.execute(sql[0], sql[1])

  # create an account for the person
  new_person_id = c.lastrowid
  sql = build_insert(('person', 'comments'), 'accounts', json.loads('{"person": ' + str(1) + ', "comments": "Auto create"}'))
  c.execute(sql[0], sql[1])
  conn.commit()
  
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
@route('/r_people/<id>', method='GET')
@auth_basic(check)
def r_people(id):
  conn = sqlite3.connect(db_name)
  c = conn.cursor()
  c.execute("DELETE FROM people WHERE id = ?", (id,))
  conn.commit()
  c.close()
  
  return {"success": True} 



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

  return template('tpl/places', items=response["items"])

# Return a listing of addresses
@route('/list_places/<format>')
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
    return template('tpl/item_table', items=response["items"])
  
  return response

# Add an address
@route('/add_places', method='POST')
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
@route('/r_places/<id>', method='GET')
@auth_basic(check)
def r_places(id):
  conn = sqlite3.connect(db_name)
  c = conn.cursor()
  c.execute("DELETE FROM places WHERE id = ?", (id,))
  conn.commit()
  c.close()
  
  return {"success": True}
  

############################################
  
application = bottle.default_app()
