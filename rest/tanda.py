import sys, os, bottle, requests, collections

#sys.path = ['/var/www/apschreiber/rest/'] + sys.path
os.chdir(os.path.dirname(__file__))

import sqlite3, json, nltk
from bottle import *
from bottle import template

############################################

def check(username, password):
  if username == password:
    return True
  return False


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


############################################
  
application = bottle.default_app()
