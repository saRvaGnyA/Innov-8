from asyncio.windows_events import NULL
import base64

import io
import profile
from PIL import Image
from frontend.users.forms import (AddProjectForm)
from frontend import db
from ast import Pass
from flask import render_template, url_for, flash, redirect, request, Blueprint
from flask_login import login_user, current_user, logout_user
from matplotlib.pyplot import table
from frontend import bcyrpt
from frontend.models import Users
from frontend.users.forms import ( AddEventForm, RegistrationForm, LoginForm,SearchUserForm)
import sqlite3
from frontend.users.forms import (AddProjectForm, CommentForm, EventRegisterForm)

from flask import Flask, render_template, url_for, flash, session,redirect, request, Blueprint
from flask_login import login_user, current_user, logout_user, login_required
import sqlite3
table_info={'1':["Student","student_name","student_email","student_password","student_id"],
            '2':["Organizer","organizer_name","organizer_email","organizer_password","organizer_id"],
            '3':["Sponsor","sponsor_name","sponsor_email","sponsor_password","sponsor_id"]
            }


def db_connection():
    conn = None
    try:
        conn = sqlite3.connect("identifier.sqlite")
    except sqlite3.error as e:
        print(e)
    return conn

def OrganizerDetail():
    conn = db_connection()
    cursor = conn.cursor()
    sql_query = '''SELECT * from Organizer'''
    cursor =cursor.execute(sql_query)
    organizerList=cursor.fetchall()
    orgDet=dict()
    for org in organizerList:
        orgDet[org[0]]=list(org[1:])
    return orgDet


def searchProject(ProjectTitle):
    conn = db_connection()
    cursor = conn.cursor()
    # tou=current_user.type_of_user
    sql_query = '''
    SELECT * FROM Project WHERE project_title = "{}"'''.format(ProjectTitle)
    cursor =cursor.execute(sql_query)
    return cursor.fetchall()   

def getProjectList(usr_det):
    conn = db_connection()
    cursor = conn.cursor()
    sql_query = '''SELECT * from ProjectLink WHERE student_id = {}'''.format(usr_det[0][0])
    cursor =cursor.execute(sql_query)
    projLinkDet=cursor.fetchall()
    if projLinkDet==[]:
        return []
    sql_query = '''SELECT * from Project WHERE project_id = {}'''.format(projLinkDet[0][0])
    cursor =cursor.execute(sql_query)
    return cursor.fetchall()    


def FollowUser(usr_det):
    conn = db_connection()
    cursor = conn.cursor()
    usr_id = userDetails()[0][0]
    # tou=current_user.type_of_user
    sql_query = '''INSERT into Follow(follower_id,following_id) values ({},{})'''.format(usr_id,usr_det[0][0])
    cursor =cursor.execute(sql_query)
    conn.commit()

def isFollowed(usr_det):
    conn = db_connection()
    cursor = conn.cursor()
    usr_id = userDetails()[0][0]
    # tou=current_user.type_of_user
    sql_query = '''SELECT * from Follow WHERE follower_id = {} AND following_id = {}'''.format(usr_id,usr_det[0][0])
    cursor =cursor.execute(sql_query)
    # conn.commit()
    # print(sql_query)
    return cursor.fetchall()    

def isSponsored():
    conn = db_connection()
    cursor = conn.cursor()
    usr_id = userDetails()[0][0]
    # tou=current_user.type_of_user
    sql_query = '''SELECT event_id from Sponsorship WHERE sponsor_id = {} '''.format(usr_id)
    cursor =cursor.execute(sql_query)
    # conn.commit()
    print(sql_query)
    return cursor.fetchall()    

# Function to retrieve events from database
def GetEvents():
    conn = db_connection()
    cursor = conn.cursor()
    sql_query = '''
    SELECT * FROM Event;
    '''
    cursor=cursor.execute(sql_query)
    print(cursor)
    return cursor.fetchall()

def userDetails():
    conn = db_connection()
    cursor = conn.cursor()
    tou=current_user.type_of_user
    sql_query = '''
    SELECT * FROM {} WHERE {} = "{}"'''.format(table_info[tou][0],table_info[tou][2],current_user.email)
    cursor =cursor.execute(sql_query)
    return cursor.fetchall()

def userDetailsLike(id,tou):
    conn = db_connection()
    cursor = conn.cursor()
    sql_query = '''SELECT * FROM {} WHERE {} = {}'''.format(table_info[tou][0],table_info[tou][4],id)
    cursor =cursor.execute(sql_query)
    # print(cursor.fetchall())
    data=cursor.fetchall()
    print(data)
    return data

def getUserList(typeofuser,Searchuser):
    conn = db_connection()
    cursor = conn.cursor()
    # tou=current_user.type_of_user
    tou=typeofuser
    sql_query = '''
    SELECT * FROM {} WHERE {} = "{}"'''.format(table_info[tou][0],table_info[tou][1],Searchuser)
    cursor =cursor.execute(sql_query)
    
    return cursor.fetchall()

def getSponsorship(id):
    conn = db_connection()
    cursor = conn.cursor()
    usr_id = userDetails()[0][0]
    # tou=current_user.type_of_user

    sql_query = '''INSERT into Sponsorship(sponsor_id,event_id) values ({},{})'''.format(usr_id,id)
    # print(sql_query)
    cursor =cursor.execute(sql_query)
    conn.commit()   

def getSponsorsList():
    conn=db_connection()
    cursor=conn.cursor()
    sql_query = '''
    SELECT * FROM Sponsor '''
    cursor =cursor.execute(sql_query)
    
    return cursor.fetchall()

def getStudentList():
    conn=db_connection()
    cursor=conn.cursor()
    sql_query = '''
    SELECT * FROM Student '''
    cursor =cursor.execute(sql_query)
    # print(cursor.fetchall())
    
    return cursor.fetchall()  

# def userProjectDetails():
#     conn = db_connection()
#     cursor=conn.cursor()
#     sql_query ='''
    
#     '''


main = Blueprint('main', __name__)
@main.route('/',methods=['GET','POST'])
@main.route('/home',methods=['GET','POST'])
def home():
    events=GetEvents()
    
    # print(current_user)
    formNew=SearchUserForm()
    return render_template('dummyEvents.html',events=events,formNew=formNew)


@main.route('/eventsList',methods=['GET','POST'])
def eventsList():
    events=GetEvents()
    org_det = OrganizerDetail()
    formNew=SearchUserForm()
    return render_template('event.html',formNew=formNew,events=events,org_det=org_det)

@main.route('/sponsorList',methods=['GET','POST'])
def sponsorList():
    formNew=SearchUserForm()
    sponsors=getSponsorsList()
    return render_template('sponsors_list.html',sponsors=sponsors,formNew=formNew)


@main.route('/editProfile',methods=['GET','POST'])
def editProfile():
    formNew=SearchUserForm()
    return render_template('edit_profile_form.html',formNew=formNew)

@main.route('/myProfile/<int:id>/<string:tou>',methods=['GET','POST'])
def myProfile(id,tou):
    #current_user = > type , id
    print(tou)
    followStatus="Followed"
    usr_det=userDetailsLike(id,tou)
    pr = isFollowed(usr_det)
    ProjInfo=getProjectList(usr_det)
    if pr==[]:
        followStatus="Follow"
    # print(usr_det)
    # usr_det=[(1,2,3,4)]
    formNew=SearchUserForm()
    return render_template('profile.html',usr_det=usr_det,id=id,tou=tou,followStatus=followStatus,ProjInfo=ProjInfo,formNew=formNew)

@main.route('/eventsForSponsor',methods=['GET','POST'])
def eventsForSponsor():
    events=GetEvents()
    org_det = OrganizerDetail()
    formNew=SearchUserForm()
    eveSponsored = isSponsored()
    eveSp=list()
    for e in eveSponsored:
        eveSp.append(e[0])
    # print(eveSp)
    # if isSponsored(id)==[]:
    #     sponsorShipStatus="Sponsor"
    # print(org_det)
    formNew=SearchUserForm()
    return render_template('event_for_sponsors.html',events=events,org_det=org_det,eveSp=eveSp,formNew=formNew)

@main.route('/account',methods=['GET','POST'])
def account():
    #current_user = > type , id
    usr_det=userDetails()
    formNew=SearchUserForm()
    return render_template('account.html',usr_det=usr_det,formNew=formNew)

@main.route('/sponsorAnEvent/<int:id>',methods=['GET','POST'])
def sponsorAnEvent(id):
    events=GetEvents()
    org_det = OrganizerDetail()
    getSponsorship(id)
    formNew=SearchUserForm()
    # print("output: ",isSponsored(id))
    # if isSponsored(id)==[]:
    #     sponsorShipStatus="Sponsor"
    # print(org_det)
    eveSponsored = isSponsored()
    eveSp=list()
    for e in eveSponsored:
        eveSp.append(e[0])
    print(eveSp)
    return render_template('event_for_sponsors.html',events=events,org_det=org_det,eveSp=eveSp,formNew=formNew)


@main.route('/project',methods=['GET','POST'])
def project():
    #current_user = > type , id
    # usr_det=userDetails()
    formNew=SearchUserForm()
    return render_template('project.html',formNew=formNew)

@main.route('/search',methods=['GET','POST'])
def search():
    #current_user = > type , id
    # usr_det=userDetails()
    form = SearchUserForm()
    # form2= FollowUser()
    if request.method=='POST':
        Searchuser=form.searchuser.data
        typeofuser=form.dropdown.data
        # print("type",typeofuser)
        userSearchResult=getUserList(typeofuser,Searchuser)
        formNew=SearchUserForm()
        return render_template('dummydisplay.html',formNew=formNew,userSearchResult=userSearchResult,form=form,typeofuser=typeofuser)

    return render_template('dummySearch.html',form=form)

# @main.route('/displayEvent')
# def displayEvent():
# return render_template('dummySearch.html',form=form)





@main.route('/create-project',methods=['GET','POST'])
def createProject():
    form=AddProjectForm()
    formNew=SearchUserForm()
    print("ProjectDes")
    if request.method=='POST':
        ProjectTitle=form.projecttitle.data
        ProjectShortDes=form.projectShortDes.data
        ProjectDes=form.projectDes.data
        DriveLink=form.driveLink.data
        byteString=form.projectImg.data.read()
        blob=base64.b64encode(byteString)
        
        print(ProjectTitle)
        print(ProjectShortDes)
        print(ProjectDes)
        print(DriveLink)
        print(blob)
        try:
            sql_query='''
            INSERT into Project({},{},{},{},{})
            values (?,?,?,?,?);
            '''.format("project_title","project_desc","project_rich_text_desc","project_drive_link","project_image_file")
            conn = db_connection()
            cursor= conn.cursor()
            cursor.execute(sql_query,(ProjectTitle,ProjectShortDes,ProjectDes,DriveLink,blob))
            
            conn.commit()
            userid=userDetails()[0][0]
            projectid=searchProject(ProjectTitle)[0][0]
            sql_query='''
            INSERT into ProjectLink(project_id,student_id) values({},{})
            '''.format(projectid,userid)
            cursor.execute(sql_query)
            print(cursor)           
            conn.commit()
        except Exception as e:
            print(e)
        return redirect('/create-project')  
    return render_template('createProject.html',form=form,formNew=formNew)

@main.route('/studentList',methods=['GET','POST'])
def studentList():
    formNew=SearchUserForm()
    stud_list=getStudentList()
    print(stud_list)
    return render_template('students_list.html',formNew=formNew,stud_list=stud_list)

@main.route('/getImage')
def getImage():
    conn = db_connection()
    cursor= conn.cursor()
    sql_query='''
    SELECT project_image_file FROM Project WHERE project_id=3;
    '''
    cursor.execute(sql_query)
    data=cursor.fetchall()
    image=data[0][0]
    return render_template('harshdum.html',image=image.decode("utf-8"))


@main.route('/follow/<int:id>/<string:tou>',methods=['GET','POST'])
def follow(id,tou):
    formNew=SearchUserForm()
    print("follow User")
    usr_det=userDetailsLike(id,tou)
    followStatus="Followed"
    usr_det=userDetailsLike(id,tou)
    ProjInfo=getProjectList(usr_det)
    if isFollowed(usr_det)==[]:
        followStatus="Follow"
    FollowUser(usr_det)
    return render_template('profile.html',usr_det=usr_det,id=id,tou=tou,followStatus=followStatus,ProjInfo=ProjInfo,formNew=formNew)



@main.route('/registerForEvent/<int:eventId>',methods=['GET','POST'])
def registerForEvent(eventId):
    form=EventRegisterForm()
    formNew=SearchUserForm()
    if request.method=='POST':
        
        conn = db_connection()
        cursor= conn.cursor()


        # CHECKING WHETHER THE TEAM NAME ALREADY EXISTS FOR THE SAME EVENT OR NOT
        sql_query='''
        SELECT * FROM Team WHERE team_name="{}" AND event_id={}
        '''.format(form.team_name.data,10)
        cursor.execute(sql_query)
        existing_team_data=cursor.fetchall()
        if len(existing_team_data)!=0:
            print('Team ALready exists')
            flash("Team name already exists for this event")
        else:
            sql_query='''
            SELECT * FROM Student WHERE student_email="{}" OR student_email="{}" OR student_email="{}" OR student_email="{}"  
            '''.format(form.member_01_email.data,form.member_02_email.data,form.member_03_email.data,form.member_04_email.data)
            try:
                # FETCHING THE TUPLES OF THE TEAM-MATES FROM THE STUDENT TABLE
                cursor.execute(sql_query)
                student_data=cursor.fetchall()
                print(student_data)

                if len(student_data)==form.number_of_members.data:
                    print("True")

                    #INSERING TEAM INTO THE TABLE 
                    sql_query_01='''
                    INSERT INTO Team({},{}) values(?,?)
                    '''.format("team_name","event_id")
                    try:
                        cursor.execute(sql_query_01,(form.team_name.data,eventId))
                        conn.commit()
                    except Exception as e:
                        print("Inserting into team table")
                        print(e)

                    #FETCHING TEAM DETAILS
                    sql_query_02='''
                    SELECT * FROM Team WHERE {}="{}"
                    '''.format("team_name",form.team_name.data)
                    cursor.execute(sql_query_02)
                    team_data=cursor.fetchone()
                    print(team_data)

                    #INSERTING THE PARTICIPANTS INTO THE PARTICIPANT TABLE
                    sql_query_03='''
                    INSERT INTO Participants({},{},{},{}) values(?,?,?,?)
                    '''.format("student_id","event_id","team_id","participation_certificate")
                    for i in range(0,len(student_data)):
                        try:
                            cursor.execute(sql_query_03,(student_data[i][0],eventId,team_data[0],"Eligible"))
                            conn.commit()
                        except Exception as e:
                            print("Inserting into partcipants table")
                            print(e)


                else:
                    print("Invalid email/emails")
            except Exception as e:
                print(e)
            return redirect('/eventsList')
    return render_template('create_team.html',form=form,formNew=formNew)

@main.route('/add-comment',methods=['GET','POST'])
def comment():
    form=CommentForm()
    formNew=SearchUserForm()
    if request.method=='POST':
        conn = db_connection()
        cursor= conn.cursor()
        sql_query='''
        SELECT student_id FROM STUDENT WHERE student_email="{}" 
        '''.format(current_user.email)
        try:
            cursor.execute(sql_query)
            data=cursor.fetchall()
            student_id=data[0][0]
            print(student_id)
            sql_query='''
            INSERT INTO Comment ({},{},{}) values(?,?,?)
            '''.format("project_id","commenter_id","comment_content")
            try:
                cursor.execute(sql_query,(2,student_id,form.comment.data))
                conn.commit()
            except Exception as e:
                print(e)
            
            sql_query='''
            INSERT INTO Participants
            '''
        except Exception as e:
            print(e)
    return render_template('comment.html',form=form,formNew=formNew)
