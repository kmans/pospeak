from pospeakapp import db
from werkzeug import generate_password_hash, check_password_hash

#tinyurl will generate unique urls based on a positive integer value
from tinyurl import encode_url, decode_url

#we will use this to create our sharing hyperlinks
from urlparse import urljoin
from flask import request

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


class Room(db.Model):
    seq = db.Column(db.Integer, primary_key=True)
    room = db.Column(db.String(10), nullable=False)
    

    def __init__(self, room):
        self.room = room


#we will need to call on tinyurl to generate a unique room for us...
#we may need to separate this onto a new process/worker

#def createRoom():
#    return binascii.hexlify(os.urandom(3))


def createRoom():


    try:
        prevroom = Room.query.order_by(db.desc(Room.seq)).first()
        newroom = Room(encode_url(prevroom.seq+1))
        db.session.add(newroom)
        db.session.commit()

    except AttributeError:
        newroom = Room(encode_url(1))
        db.session.add(newroom)
        db.session.commit()

    return newroom.room

def make_url(room):
    return urljoin(request.url_root, room)