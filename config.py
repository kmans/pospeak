SECRET_KEY = 'SECRET_KEY'
DEBUG = True
#DEBUG = False
SQLALCHEMY_DATABASE_URI = 'sqlite:///pospeak.db'
SQLALCHEMY_BINDS = {'users':'sqlite:///users.db'}
STATIC_ROOT = None