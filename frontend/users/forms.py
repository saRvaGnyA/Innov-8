from multiprocessing import Event
from wsgiref.validate import validator
from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed,FileRequired
from wtforms import StringField, PasswordField, SubmitField, BooleanField, SelectField, DateField,TextAreaField
from flask_wtf.file import FileField, FileRequired
from wtforms import StringField, PasswordField, SubmitField, BooleanField, SelectField, DateField,IntegerField
from markupsafe import Markup
from wtforms.widgets import SubmitInput
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError
from flask_login import current_user
from frontend.models import Users
import sqlite3


def db_connection():
    conn = None
    try:
        conn = sqlite3.connect("identifier.sqlite")
    except sqlite3.error as e:
        print(e)
    return conn

def GetEventsTypes():
    conn = db_connection()
    cursor = conn.cursor()
    sql_query = '''
    SELECT * FROM EventType;
    '''
    cursor=cursor.execute(sql_query)
    print(cursor)
    return cursor.fetchall()


# class FollowUser(FlaskForm):
#     # User_choices= [('1','Student'),('2','Organizer'),('3','Sponsor')]
#     # dropdown=SelectField(u'Hour',choices=User_choices)
#     # searchuser = StringField('Project Title',validators=[DataRequired()])
#     follow=SubmitField('Follow')

# class SearchEvent(FlaskForm):
#     searchuser = StringField('Project Title',validators=[DataRequired()])
#     submit=SubmitField('Add')   



class SearchUserForm(FlaskForm):
    User_choices= [('1','Student'),('2','Organizer'),('3','Sponsor')]
    dropdown=SelectField(u'Hour',choices=User_choices)
    searchuser = StringField('Project Title',validators=[DataRequired()])
    submit=SubmitField('Search')

class AddProjectForm(FlaskForm):
    # Event_choices= GetEventsTypes()
    # eventsdropdown=SelectField(u'Events',choices=Event_choices)
    projecttitle = StringField('Project Title',validators=[DataRequired()])
    projectShortDes = StringField('Project Description',validators=[DataRequired()])
    projectDes = StringField('Project Description',validators=[DataRequired()])
    driveLink = StringField('drive link',validators=[DataRequired()])
    richText = StringField('rich text',validators=[DataRequired()])
    projectImg = FileField('images',validators=[FileRequired(),])
    # eventloc = StringField('Event Location',validators=[DataRequired()])
    # eventdec = StringField('Event Description',validators=[DataRequired()])
    submit=SubmitField('Add Project')

class AddEventForm(FlaskForm):
    Event_choices= GetEventsTypes()
    eventsdropdown=SelectField(u'Events',choices=Event_choices)
    eventstartdate = DateField('StartDate',validators=[DataRequired()])
    eventenddate = DateField('StartDate',validators=[DataRequired()])
    eventloc = StringField('Event Location',validators=[DataRequired()])
    eventdec = StringField('Event Description',validators=[DataRequired()])
    submit=SubmitField('Add')


class RegistrationForm(FlaskForm):
    User_choices= [('1','Student'),('2','Organizer'),('3','Sponsor')]
    dropdown=SelectField(u'Hour',choices=User_choices)
    username = StringField('Username',validators=[DataRequired(), Length(min=2, max=20)])
    email = StringField('Email',validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    confirm_password = PasswordField('Confirm Password',validators=[DataRequired(), EqualTo('password')])
    submit=SubmitField()


class LoginForm(FlaskForm):
    User_choices= [('1','Student'),('2','Organizer'),('3','Sponsor')]
    dropdown=SelectField(u'Hour',choices=User_choices)
    email = StringField('Email',validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember = BooleanField('Remember Me')
    submit = SubmitField('Login')


# class UpdateAccountForm(FlaskForm):
#     username = StringField('Username',
#                            validators=[DataRequired(), Length(min=2, max=20)])
#     email = StringField('Email',
#                         validators=[DataRequired(), Email()])
#     picture = FileField('Update Profile Picture', validators=[FileAllowed(['jpg', 'png'])])
#     submit = SubmitField('Update')

#     def validate_username(self, username):
#         if username.data != current_user.username:
#             user = User.query.filter_by(username=username.data).first()
#             if user:
#                 raise ValidationError('That username is taken. Please choose a different one.')

#     def validate_email(self, email):
#         if email.data != current_user.email:
#             user = User.query.filter_by(email=email.data).first()
#             if user:
#                 raise ValidationError('That email is taken. Please choose a different one.')


# class RequestResetForm(FlaskForm):
#     email = StringField('Email',
#                         validators=[DataRequired(), Email()])
#     submit = SubmitField('Send Reset Link',validators=[DataRequired()])

#     def validate_email(self, email):
#         user = User.query.filter_by(email=email.data).first()
#         if user is None:
#             raise ValidationError('There is no account with that email. You must register first.')


# class ResetPasswordForm(FlaskForm):
#     password = PasswordField('Password', validators=[DataRequired()])
#     confirm_password = PasswordField('Confirm Password',
#                                      validators=[DataRequired(), EqualTo('password')])
#     submit = SubmitField('Reset Password')


class EventRegisterForm(FlaskForm):
    team_name=StringField("Team name",validators=[DataRequired()])
    number_of_members=IntegerField("Number of Teammates",validators=[DataRequired()])
    member_01_email=StringField('Email of Team Member 1',validators=[DataRequired()])
    member_02_email=StringField('Email of Team Member 2')
    member_03_email=StringField('Email of Team Member 3')
    member_04_email=StringField('Email of Team Member 4')
    submit=SubmitField('Make Team')

class CommentForm(FlaskForm):
    comment=StringField("Comment",validators=[DataRequired()])
    submit=SubmitField("Comment")