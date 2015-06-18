from flask import render_template, url_for, redirect, flash, request, session

from pospeakapp import app, db
from pospeakapp.models import Comment, User, createRoom, make_url
from pospeakapp.forms import CommentForm, UserForm, LoginForm

import datetime
import urlparse


@app.route('/login', methods=['GET', 'POST'])
def login():


  #we first check if user has a session cookie and is logged in
  if 'email' in session:
      user = User.query.filter_by(email = session['email']).first()

      #We implement a try/except catch here in the event we have a freshly
      #created database and the user will be of type None with no email attr
      try:
        email = user.email
      except AttributeError:
        user = None
        #email = "Anonymous"
  
  else:
      user = None
      #email = "Anonymous"

  form = LoginForm()
   
  if request.method == 'POST':
    if form.validate() == False:
      return render_template('login.html', form=form)
    else:
      session['email'] = form.email.data
      flash(form.email.data + " successfully logged in!")
      return redirect(url_for('index'))
                 
  elif request.method == 'GET':
    return render_template('login.html', form=form, user=user)


@app.route('/logout')
def logout():
 
  if 'email' not in session:
    flash("Logout Successful")
    return redirect(url_for('index'))
     
  session.pop('email', None)
  flash("Logout Successful")
  return redirect(url_for('index'))

@app.route('/signup', methods=['GET', 'POST'])
def signup():

  #we first check if user has a session cookie and is logged in
  if 'email' in session:
      user = User.query.filter_by(email = session['email']).first()

      #We implement a try/except catch here in the event we have a freshly
      #created database and the user will be of type None with no email attr
      try:
        email = user.email
      except AttributeError:
        user = None
        #email = "Anonymous"
  
  else:
      user = None
      #email = "Anonymous"

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

        flash("Registration successful for " + form.email.data) 
        return redirect(url_for('index'))

   
  elif request.method == 'GET':
    return render_template('signup.html', form=form, user=user)


@app.route('/', methods=['GET', 'POST'])
@app.route('/<room>', methods=['GET', 'POST'])
def index(room='home'):

    #we first check if user has a session cookie and is logged in
    if 'email' in session:
        user = User.query.filter_by(email = session['email']).first()

        #We implement a try/except catch here in the event we have a freshly
        #created database and the user will be of type None with no email attr
        try:
          email = user.email
        except AttributeError:
          user = None
          email = "Anonymous"
    
    else:
        user = None
        email = "Anonymous"
        
    
    form = CommentForm()
    if form.validate_on_submit():
        comment = Comment(
            form.text.data,
            datetime.datetime.now(),
            room,
            email
        )
        db.session.add(comment)
        db.session.commit()
        flash("comment added on " + 
              comment.timestamp.strftime('%Y-%m-%d %H:%M:%S') + 
              " for room " + room + " by " + email)
        return redirect(url_for('index', room=room))


    
    comments = Comment.query.filter_by(room=room).order_by(
        db.asc(Comment.timestamp))
    ccount = comments.count()
    return render_template('index.html', comments=comments, form=form, 
                           room=room, new=createRoom(), ccount=ccount, user=user, url=make_url(room))


def static(path):
    root = app.config.get('STATIC_ROOT')
    if root is None:
        return url_for('static', filename=path)
    else:
        return urlparse.urljoin(root, path)

@app.context_processor
def context_processor():
    return dict(static=static)