from pospeakapp.models import Comment, User

#WTForms / Flask-WTForms
from flask.ext.wtf import Form
from wtforms import TextField, PasswordField, SubmitField, validators

#Form for the chatroom
class CommentForm(Form):
    text = TextField('Comment', [validators.Required()])


#In the future we will implement a username-type field...
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

#We only will require email address and password for logon, so we must create 
#a new class for just this purpose
class LoginForm(Form):
    email = TextField('Email Address', [validators.Required("Please enter your email address."), validators.Email("Please enter your email address")])
    password = PasswordField('Password', [validators.Required("Please enter a valid password")])
    submit = SubmitField("Login")

    def __init__(self, *args, **kwargs):
        Form.__init__(self, *args, **kwargs)

    def validate(self):
        if not Form.validate(self):
            return False
     
        user = User.query.filter_by(email = self.email.data.lower()).first()
        if user and user.check_password(self.password.data):
            return True
        else:
            self.email.errors.append("Invalid e-mail or password")
            return False