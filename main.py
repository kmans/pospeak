from flask import Flask, render_template, url_for, redirect, flash

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
    def __init__(self, text, timestamp):
        self.text = text
        self.timestamp = timestamp


#Form for the textfield
class CommentForm(Form):
    text = TextField('Comment', [validators.Required()])



@app.route('/', methods=['GET', 'POST'])
@app.route('/<int:chatsession>', methods=['GET', 'POST'])
def index(chatsession=0):
    form = CommentForm()
    if form.validate_on_submit():
        comment = Comment(
            form.text.data,
            datetime.datetime.now()
        )
        db.session.add(comment)
        db.session.commit()
        flash("comment added on " + comment.timestamp.strftime('%Y-%m-%d %H:%M:%S'))
        return redirect(url_for('index', chatsession=chatsession))
    comments = Comment.query.order_by(db.desc(Comment.timestamp))
    return render_template('index.html', comments=comments, form=form)


def static(path):
    root = app.config.get('STATIC_ROOT')
    if root is None:
        return url_for('static', filename=path)
    else:
        return urlparse.urljoin(root, path)

@app.context_processor
def context_processor():
    return dict(static=static)





app.run(debug=True)
