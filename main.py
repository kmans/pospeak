from flask import Flask, render_template, url_for, redirect, flash


#for random chatroom hash
import binascii
import os


#For db
from flask.ext.sqlalchemy import SQLAlchemy

#WTForms / Flask-WTForms
from flask.ext.wtf import Form
from wtforms import TextField, validators

import datetime
import urlparse


app = Flask(__name__)

app.config.update(
	SECRET_KEY = '3ivwmZUQ5uJEpqI4YX99D05Q8IaLPz0o',
	DEBUG = True,
	SQLALCHEMY_DATABASE_URI = 'sqlite:///pospeak.db',
	STATIC_ROOT = None
	)

db = SQLAlchemy(app)
db.create_all()




#primary db model
class Comment(db.Model):
    comment_id = db.Column(db.Integer, primary_key=True)
    text = db.Column(db.Text, nullable=False)
    timestamp = db.Column(db.DateTime, nullable=False)
    room = db.Column(db.Text, nullable=False)

    def __init__(self, text, timestamp, room):
        self.text = text
        self.timestamp = timestamp
        self.room = room





#generate a very random hex value
def createRoom():
    return binascii.hexlify(os.urandom(3))


#Form for the textfield
class CommentForm(Form):
    text = TextField('Comment', [validators.Required()])



@app.route('/', methods=['GET', 'POST'])
@app.route('/<room>', methods=['GET', 'POST'])
def index(room='000000'):
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
    return render_template('index.html', comments=comments, form=form, room=room, new=createRoom(), ccount=ccount)


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
