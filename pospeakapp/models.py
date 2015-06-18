
from pospeakapp import db
from werkzeug import generate_password_hash, check_password_hash

#We will use these for room generation until tinyurl is implemented
import binascii
import os
#from tinyurl import encode_url, decode_url


#primary db model for Comments
class Comment(db.Model):
    comment_id = db.Column(db.Integer, primary_key=True)
    text = db.Column(db.Text, nullable=False)
    timestamp = db.Column(db.DateTime, nullable=False)
    room = db.Column(db.String(60), nullable=False)
    email = db.Column(db.String(80))

    def __init__(self, text, timestamp, room, email):
        self.text = text
        self.timestamp = timestamp
        self.room = room
        self.email = email


#SQLAlchemy bind: 'users' // for login data - keep in separate DB
class User(db.Model):
    __bind_key__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(80), unique=True)
    pwdhash = db.Column(db.String(80), nullable=False)

    def __init__(self, email, password):
        self.email = email.lower()
        self.set_password(password)

    def set_password(self, password):
        self.pwdhash = generate_password_hash(password)
   
    def check_password(self, password):
        return check_password_hash(self.pwdhash, password)


#we will need to call on tinyurl to generate a unique room for us...
#we may need to separate this onto a new process/worker

def createRoom():
    return binascii.hexlify(os.urandom(3))


