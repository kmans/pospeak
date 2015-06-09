from flask import Flask, render_template, url_for, redirect, flash, request, session

#for random chatroom hash
import binascii
import os


#For db
from flask.ext.sqlalchemy import SQLAlchemy

#For user login / session management / password hashing
from werkzeug import generate_password_hash, check_password_hash


#WTForms / Flask-WTForms
from flask.ext.wtf import Form
from wtforms import TextField, PasswordField, SubmitField, validators

import datetime
import urlparse


app = Flask(__name__)

app.config.update(
	SECRET_KEY = '3ivwmZUQ5uJEpqI4YX99D05Q8IaLPz0o',
	DEBUG = True,
	SQLALCHEMY_DATABASE_URI = 'sqlite:///pospeak.db',
    SQLALCHEMY_BINDS = {
    'users':        'sqlite:///users.db'
    },
	STATIC_ROOT = None
	)

#initialize SQLAlchemy db to work with our flask app
db = SQLAlchemy(app)


#primary db model for Comments
class Comment(db.Model):
    comment_id = db.Column(db.Integer, primary_key=True)
    text = db.Column(db.Text, nullable=False)
    timestamp = db.Column(db.DateTime, nullable=False)
    room = db.Column(db.Text, nullable=False)

    def __init__(self, text, timestamp, room):
        self.text = text
        self.timestamp = timestamp
        self.room = room


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


#create all the databases
db.create_all()

#Do we need to commit here? Uncomment if we do.
#db.session.commit()



#generate a very random hex value
def createRoom():
    return binascii.hexlify(os.urandom(3))


#Form for the chatroom
class CommentForm(Form):
    text = TextField('Comment', [validators.Required()])


class UserForm(Form):
    email = TextField('Email Address', [validators.Required("Please enter your email address."), validators.Email("Please enter your email address")])
    password = PasswordField('Password', [validators.Required("Please enter a valid password")])
    submit = SubmitField("Create account")

    def __init__(self, *args, **kwargs):
        Form.__init__(self, *args, **kwargs)
 
    def validate(self):
        if not Form.validate(self):
          return False
     
        user = User.query.filter_by(email = self.email.data.lower()).first()
        if user:
            self.email.errors.append("That email is already taken")
            return False
        else:
            return True



@app.route('/signup', methods=['GET', 'POST'])
def signup():
  form = UserForm()
   
  if request.method == 'POST':
    if form.validate() == False:
      return render_template('signup.html', form=form)
    else:

        form.password.data    
        newuser = User(form.email.data, form.password.data)
        db.session.add(newuser)
        db.session.commit()

        session['email'] = newuser.email

        return redirect(url_for('index'))

   
  elif request.method == 'GET':
    return render_template('signup.html', form=form)




'''
@app.route('/login', methods=['GET', 'POST'])
def login():

    form = UserForm()
    if form.validate_on_submit():
        userdata = User(
            form.email.data,
            form.password.data,
            form.remember.data
        )
        db.session.add(userdata)
        db.session.commit()
        flash("Successfully logged in!")
        return redirect(url_for('index'))

    return render_template('login.html', form=form)
'''


@app.route('/', methods=['GET', 'POST'])
@app.route('/<room>', methods=['GET', 'POST'])
def index(room='000000'):

    #we first check if user has a session cookie and is logged in
    if 'email' in session:
        user = User.query.filter_by(email = session['email']).first()
    else:
        user = None
    
    form = CommentForm()
    if form.validate_on_submit():
        comment = Comment(
            form.text.data,
            datetime.datetime.now(),
            room
        )
        db.session.add(comment)
        db.session.commit()
        flash("comment added on " + comment.timestamp.strftime('%Y-%m-%d %H:%M:%S') + " for room " + room)
        return redirect(url_for('index', room=room))
    
    comments = Comment.query.filter_by(room=room).order_by(db.desc(Comment.timestamp))
    ccount = comments.count()
    return render_template('index.html', comments=comments, form=form, room=room, new=createRoom(), ccount=ccount, user=user)


def static(path):
    root = app.config.get('STATIC_ROOT')
    if root is None:
        return url_for('static', filename=path)
    else:
        return urlparse.urljoin(root, path)

@app.context_processor
def context_processor():
    return dict(static=static)



if __name__ == "__main__":

    #app.run(debug=True)
    app.run()
