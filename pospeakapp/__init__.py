from flask import Flask
from flask.ext.sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config.from_object('config')

'''
app.config.update(
	SECRET_KEY = '3ivwmZUQ5uJEpqI4YX99D05Q8IaLPz0o',
	DEBUG = True,
	SQLALCHEMY_DATABASE_URI = 'sqlite:///pospeak.db',
    SQLALCHEMY_BINDS = {
    'users':        'sqlite:///users.db'
    },
	STATIC_ROOT = None
	)
'''

#initialize SQLAlchemy db to work with our flask app
db = SQLAlchemy(app)

#import the MVC
import pospeakapp.models
import pospeakapp.forms

#setup the db and configure the tables
db.create_all()

import pospeakapp.views