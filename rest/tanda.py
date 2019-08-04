import sys, os, bottle, requests, collections

#sys.path = ['/var/www/apschreiber/migrations/'] + sys.path
os.chdir(os.path.dirname(__file__))

import sqlite3, json, nltk
from bottle import *
from bottle import template

############################################

db_name = 'tanda.db'

people_cols = ('eto', 'first', 'last', 'middle', 'suffix', 'email', 'phone', 'dob', 'description')
places_cols = ('address1', 'address2', 'city', 'state', 'zip', 'country', 'description', 'comments')

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

### People ###

@route('/list_people/<format>')
def listPeople(format):

  conn = sqlite3.connect(db_name)
  c = conn.cursor()
  c.execute("SELECT id, eto, first, last, middle, suffix, email, phone, dob, description FROM people")
  #c.execute("SELECT * FROM people")
  result = c.fetchall()
  c.close()
  response = {}
  response["items"] = []
  for r in result:
    item = dict_builder(("id",) + people_cols, r)
    response["items"].append(item)
  
  if format == 'table':
    return template('tpl/item_table', items=response["items"])
  
  return response

@route('/add_people', method='POST')
def add_people():
  data = request.json
  conn = sqlite3.connect(db_name)
  c = conn.cursor()
  sql = build_insert(people_cols, "people", request.json)
  c.execute(sql[0], sql[1])
  conn.commit()
  
  return {"success": True}

@route('/people/<id>', method='GET')
def people(id):
  conn = sqlite3.connect(db_name)
  c = conn.cursor()
  c.execute(build_select(people_cols, 'people', "id = ?"), (id,))
  result = c.fetchall()
  c.close()
  
  return response_dict(result, people_cols)
  
@route('/people/<id>', method='POST')
def edit_people(id):
  data = request.json
  conn = sqlite3.connect(db_name)
  c = conn.cursor()
  sql = build_update(people_cols, "people", data, id)
  c.execute(sql)
  conn.commit()
  
  return {"success": True}

@route('/r_people/<id>', method='GET')
@auth_basic(check)
def r_people(id):
  conn = sqlite3.connect(db_name)
  c = conn.cursor()
  c.execute("DELETE FROM people WHERE id = ?", (id,))
  conn.commit()
  c.close()
  
  return {"success": True} 


### Places ###

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

@route('/add_places', method='POST')
def add_places():
  data = request.json
  conn = sqlite3.connect(db_name)
  c = conn.cursor()
  sql = build_insert(places_cols, "places", request.json)
  c.execute(sql[0], sql[1])
  conn.commit()
  
  return {"success": True}

@route('/places/<id>', method='GET')
def places(id):
  conn = sqlite3.connect(db_name)
  c = conn.cursor()
  c.execute(build_select(places_cols, 'places', "id = ?"), (id,))
  result = c.fetchall()
  c.close()
  
  return response_dict(result, places_cols)
  
@route('/places/<id>', method='POST')
def edit_places(id):
  data = request.json
  conn = sqlite3.connect(db_name)
  c = conn.cursor()
  sql = build_update(places_cols, "places", data, id)
  c.execute(sql)
  conn.commit()
  
  return {"success": True}

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
