# Import flask and template operators
from flask import Flask
# import sqlalchemy as SQLAlchemy
from flask.ext.sqlalchemy import SQLAlchemy

# Define the WSGI application object
# DATABASE = './flaskr.db'
# SQLALCHEMY_DATABASE_URI = 'sqlite:///flaskr.db'
# DEBUG = True
# SECRET_KEY = 'admin'
# USERNAME = 'admin'
# PASSWORD = 'admin'



FLASK = Flask(__name__, static_url_path='/')

# FLASK.config['DATABASE'] = '/tmp/flaskr.db'
# FLASK.config['DEBUG'] = True
# FLASK.config['USERNAME'] = 'admin'
# FLASK.config['PASSWORD'] = 'admin'
# FLASK.config['SECRET_KEY'] = 'admin'

# Configurations
# FLASK.config.from_object(__name__)
# FLASK.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///flaskr.db'
# Define the database object which is imported
# by modules and controllers
# DB = SQLAlchemy(FLASK)

# Import a module
# from mod_suggest import controllers

from src.mod_suggest import controllers