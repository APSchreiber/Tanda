import sys, os, bottle, requests, collections

#sys.path = ['/var/www/apschreiber/migrations/'] + sys.path
os.chdir(os.path.dirname(__file__))

import sqlite3, json, nltk
from bottle import *
from bottle import template

############################################

db_name = 'tanda.db'

people_cols = ('first', 'last', 'middle', 'suffix', 'email', 'phone', 'dob', 'description')

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

@route('/people/<format>')
def listPeople(format):

  conn = sqlite3.connect(db_name)
  c = conn.cursor()
  c.execute("SELECT id, first, last, middle, suffix, email, phone, dob, description FROM people")
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
def add_venue():
  data = request.json
  conn = sqlite3.connect(db_name)
  c = conn.cursor()
  sql = build_insert(people_cols, "people", request.json)
  c.execute(sql[0], sql[1])
  conn.commit()
  
  return {"success": True}

############################################
  
application = bottle.default_app()
