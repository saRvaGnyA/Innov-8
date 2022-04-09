from frontend import db
from ast import Pass
from flask import render_template, url_for, flash, redirect, request, Blueprint
from flask_login import login_user, current_user, logout_user
from matplotlib.pyplot import table
from frontend import bcyrpt
from frontend.models import Users
from frontend.users.forms import ( AddEventForm, RegistrationForm, LoginForm)
import sqlite3


users = Blueprint('users', __name__)

def db_connection():
    conn = None
    try:
        conn = sqlite3.connect("identifier.sqlite")
    except sqlite3.error as e:
        print(e)
    return conn



@users.route('/addEvent',methods=['GET','POST'])
def addEvent():
    form= AddEventForm()
    if request.method=='POST':
            # Usertype=form.dropdown.data
            EventType=form.eventsdropdown.data
            Eventstartdate=form.eventstartdate.data      
            Eventenddate=form.eventenddate.data      
            EventLocation=form.eventloc.data      
            EventDescription=form.eventdec.data   
            # print(EventType,Eventstartdate,Eventenddate,EventLocation,EventDescription)
            conn = db_connection()
            cursor = conn.cursor()
            print("correct1")
            print(Eventstartdate,Eventenddate)
            sql_query = '''INSERT INTO Event(event_type_id,organizer_id,event_start_date,event_end_date,event_location,event_description) values ({},1,'{}','{}',"{}","{}");'''.format(int(EventType),Eventstartdate,Eventenddate,EventLocation,EventDescription)
            cursor.execute(sql_query)
            conn.commit()
            return redirect('/addEvent') 
    return render_template('addEvent.html',form=form)

@users.route('/login',methods=['GET','POST'])
def login():
    form=LoginForm()
    if request.method=='POST':
            Usertype=form.dropdown.data
            Email=form.email.data
            Password=form.password.data
            conn = db_connection()
            table_info={'1':["Student","student_name","student_email","student_password"],
            '2':["Organizer","organizer_name","organizer_email","organizer_password"],
            '3':["Sponsor","sponsor_name","sponsor_email","sponsor_password"]
            }
            cursor= conn.cursor()
            cursor.execute('''SELECT * FROM {} WHERE {} = "{}"'''.format(table_info[Usertype][0],table_info[Usertype][2],Email))
            user2=cursor.fetchall()
            users = Users.query.filter_by(email=form.email.data,type_of_user=Usertype).first()
            
            print("outside password")
            for r in user2:
                if bcyrpt.check_password_hash(r[3],Password) and users:
                    print("inside password")
                    login_user(users)
                    # for p in users:
                    #     print(p)
                    print("User:",users.id)
                    print("User:",users.type_of_user)
                    print("User:",users.email)
                    print(type(int(users.type_of_user)))
                    if int(users.type_of_user)==1:
                        return redirect('/eventsList')
                    elif int(users.type_of_user)==3:
                        return redirect('/eventsForSponsor')
                    else:
                        return redirect('/account')
                else:
                    flash('Login Unsuccessful. Please check email and password', 'danger')

    return render_template('login.html',form=form)

@users.route('/register',methods=['GET','POST'])
def register():
    form=RegistrationForm()
    if request.method=='POST':
        Usertype=form.dropdown.data
        print(Usertype)
        Username=form.username.data
        Email=form.email.data
        Password= bcyrpt.generate_password_hash(form.password.data).decode('utf-8')
        conn = db_connection()
        print("Outside try")
        table_info={'1':["Student","student_name","student_email","student_password"],
        '2':["Organizer","organizer_name","organizer_email","organizer_password"],
        '3':["Sponsor","sponsor_name","sponsor_email","sponsor_password"]
        }
        
        # connection_obj = sqlite3.connect('site.db')
        # cursor_obj = connection_obj.cursor()
        # cursor_obj.execute("DROP TABLE IF EXISTS users")
        # # Creating table
        # table = """ CREATE TABLE users(id INTEGER PRIMARY KEY AUTOINCREMENT,type_of_user TEXT NOT NULL,email TEXT NOT NULL); """
        # cursor_obj.execute(table)
        # connection_obj.commit()
        # connection_obj.close()

        try:
            print("Inside try")
            user = Users(type_of_user=Usertype, email=Email)
            print(user.type_of_user,user.email)
            # db.drop_all()
            db.session.add(user)
            db.session.commit()
            cursor= conn.cursor()
            sql_query = '''
            INSERT into {}({},{},{})
            values (?,?,?);
            '''.format(table_info[Usertype][0],table_info[Usertype][1],table_info[Usertype][2],table_info[Usertype][3])
            cursor.execute(sql_query,(Username,Email,Password))
            conn.commit()
            return redirect('/login')
        except Exception as e:
            print(e)   
            flash("User already exists")
        

    return render_template('register.html',form=form)