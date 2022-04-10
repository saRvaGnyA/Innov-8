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
from frontend.users.forms import (EditProfile, AddEventForm, RegistrationForm, LoginForm,SearchUserForm,Message)
import sqlite3
from frontend.users.forms import (AddProjectForm, CommentForm, EventRegisterForm,studentToSubmitProject)

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
    sql_query = '''INSERT into Follow(follower_id,following_id) values ({},{})'''.format( usr_det[0][0], usr_id)
    cursor =cursor.execute(sql_query)
    conn.commit()

def isFollowed(usr_det):
    conn = db_connection()
    cursor = conn.cursor()
    usr_id = userDetails()[0][0]
    # tou=current_user.type_of_user
    sql_query = '''SELECT * from Follow WHERE follower_id = {} AND following_id = {}'''.format(usr_det[0][0], usr_id)
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

def sendMessage(to_id,msg):
    conn = db_connection()
    cursor = conn.cursor()
    usr_id = userDetails()[0][0]
    # tou=current_user.type_of_user

    sql_query = '''INSERT into Message(user_id,user_msg ,to_id) values ({},"{}",{})'''.format(usr_id,msg,to_id)
    print(sql_query)
    cursor =cursor.execute(sql_query)
    conn.commit()      

# def userProjectDetails():
#     conn = db_connection()
#     cursor=conn.cursor()
#     sql_query ='''
    
#     '''

def getMessage(to_id):
    conn = db_connection()
    cursor = conn.cursor()
    usr_id = userDetails()[0][0]
    sql_query='''SELECT * from Message WHERE user_id = {} and to_id = {} UNION SELECT * from Message WHERE user_id ={} and  to_id = {}'''.format(usr_id,to_id,to_id,usr_id)
    # print(sql_query)
    cursor =cursor.execute(sql_query)
    ans =cursor.fetchall()
    # print(ans)
    return ans

  

def getOrganizerList():
    conn=db_connection()
    cursor=conn.cursor()
    sql_query = '''
    SELECT * FROM Organizer '''
    cursor =cursor.execute(sql_query)
    return cursor.fetchall()


main = Blueprint('main', __name__)
@main.route('/',methods=['GET','POST'])
@main.route('/home',methods=['GET','POST'])
def home():
    events=GetEvents()
    
    # print(current_user)
    formNew=SearchUserForm()
    return render_template('landing.html')


@main.route('/displayProjects/<int:pId>')
def displayProjects(pId):
    conn=db_connection()
    cursor=conn.cursor()
    sql_query ='''
    SELECT * FROM Project where project_id = {}
    '''.format(pId)
    cursor=cursor.execute(sql_query)
    formNew=SearchUserForm()
    prjDetails=cursor.fetchall()
    stdID=userDetails()[0][1]
    return render_template('project_revamp.html', prjDetails=prjDetails, stdID=stdID, formNew=formNew)



@main.route('/sendMsg/<int:to_id>/<string:personName>',methods=['GET','POST'])
def sendMsg(to_id,personName):
    formNew=SearchUserForm()
    form=Message()
    msg=form.message.data
    sendMessage(to_id,msg)
    msgList = getMessage(to_id)
    return render_template('inbox.html',formNew=formNew,to_id=to_id,form=form,msgList=msgList,personName=personName)

@main.route('/eventsList',methods=['GET','POST'])
def eventsList():
    events=GetEvents()
    org_det = OrganizerDetail()
    formNew=SearchUserForm()
    return render_template('event.html',formNew=formNew,events=events,org_det=org_det)

@main.route('/inbox/<int:to_id>/<string:personName>',methods=['GET','POST'])
def inbox(to_id,personName):
    formNew=SearchUserForm()
    form=Message()
    # msg=form.message.data
    # print(msg)
    # sendMessage(to_id,msg)
    msgList=getMessage(to_id)
    # print(msgList)
    return render_template('inbox.html',formNew=formNew,to_id=to_id,form=form,msgList=msgList,personName=personName)


@main.route('/sponsorList',methods=['GET','POST'])
def sponsorList():
    formNew=SearchUserForm()
    sponsors=getSponsorsList()
    return render_template('sponsors_list.html',sponsors=sponsors,formNew=formNew)



@main.route('/editProfile',methods=['GET','POST'])
def editProfile():
    formNew=SearchUserForm()
    form=EditProfile()
    if request.method=='POST':
        stud_name=form.stud_name.data
        stud_email=form.stud_email.data
        stud_des=form.stud_des.data
        stud_interest=form.stud_interest.data

        list_of_interest=stud_interest.split(",")
        conn = db_connection()
        cursor=conn.cursor()
        sql_query='''
        UPDATE Student 
        SET student_desc ="{}" WHERE student_id={}
        '''.format(stud_des,userDetails()[0][0])
        cursor.execute(sql_query)
       
        current_user.email=stud_email

        return redirect('/account')
    return render_template('edit_profile_form.html',formNew=formNew,form=form)

@main.route('/myProfile/<int:id>/<string:tou>',methods=['GET','POST'])
def myProfile(id,tou):
    #current_user = > type , id
    # print(tou)
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
    conn=db_connection()
    cursor=conn.cursor()
    sql_query='''SELECT count(follower_id) from Follow where following_id ={}'''.format(userDetails()[0][0])
    follow_num=cursor.execute(sql_query).fetchall()[0]
    sql_query = '''SELECT count(following_id) from Follow where follower_id ={}'''.format(userDetails()[0][0])
    following_num = cursor.execute(sql_query).fetchall()[0]
    sql_query = '''SELECT count(project_id) from ProjectLink where student_id ={}'''.format(userDetails()[0][0])
    proj_num = cursor.execute(sql_query).fetchall()[0]
    ProjInfo=getProjectList(usr_det)
    # print(ProjInfo)
    formNew=SearchUserForm()
    return render_template('account.html',ProjInfo=ProjInfo,proj_num=proj_num, usr_det=usr_det, formNew=formNew, follow_num=follow_num, following_num=following_num)

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
    # print(eveSp)
    return render_template('event_for_sponsors.html',events=events,org_det=org_det,eveSp=eveSp,formNew=formNew)


@main.route('/project',methods=['GET','POST'])
def project():
    #current_user = > type , id
    # usr_det=userDetails()
    formNew=SearchUserForm()
    
    return render_template('project_revamp.html',formNew=formNew)

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
        # return redirect('/studentList',formNew=formNew,userSearchResult=userSearchResult,form=form,typeofuser=typeofuser)
        if typeofuser=='1':
            return render_template('studentSearch.html',formNew=formNew,userSearchResult=userSearchResult,form=form,typeofuser=typeofuser)
        return redirect('/sponsorList')

    return render_template('dummySearch.html',form=form)

# @main.route('/displayEvent')
# def displayEvent():
# return render_template('dummySearch.html',form=form)





@main.route('/create-project',methods=['GET','POST'])
def createProject():
    form=AddProjectForm()
    formNew=SearchUserForm()
    # print("ProjectDes")
    if request.method=='POST':
        ProjectTitle=form.projecttitle.data
        ProjectShortDes=form.projectShortDes.data
        ProjectDes=form.projectDes.data
        DriveLink=form.driveLink.data
        byteString=form.projectImg.data.read()
        blob=base64.b64encode(byteString)
        
        try:
            sql_query='''
            INSERT into Project({},{},{},{},{})
            values (?,?,?,?,?);
            '''.format("project_title","project_desc","project_rich_text_desc","project_drive_link","project_image_file")
            conn = db_connection()
            cursor= conn.cursor()
            cursor.execute(sql_query,(ProjectTitle,ProjectShortDes,ProjectDes,DriveLink,blob))
            conn.commit()
            
            sql_query='''
            SELECT * FROM Student where student_email="{}"
            '''.format(current_user.email)
            cursor.execute(sql_query)
            submitter=cursor.fetchone()[0]

            # print(submitter)

            sql_query='''
            SELECT * FROM Project WHERE project_title="{}"
            '''.format(ProjectTitle)

            cursor.execute(sql_query)
            ProjectDatas=cursor.fetchone()
            project=ProjectDatas[0]

            sql_query='''
            INSERT INTO ProjectLink(project_id,student_id) VALUES(?,?)
            '''
            # print(submitter,project)
            cursor.execute(sql_query,(project,submitter))
            conn.commit()

            DATA=ProjectDatas[5]
            image=DATA[0][0]

            return redirect('/account')
        except Exception as e:
            print(e)
        return redirect('/account')  
    return render_template('createProject.html',form=form,formNew=formNew)

@main.route('/studentList',methods=['GET','POST'])
def studentList():
    formNew=SearchUserForm()
    stud_list=getStudentList()
    # print(stud_list)
    return render_template('students_list.html',formNew=formNew,stud_list=stud_list)

@main.route('/organizerList',methods=['GET','POST'])
def organizerList():
    formNew=SearchUserForm()
    organizer_list=getOrganizerList()
    # print(organizer_list)
    return render_template('organizers_list.html',formNew=formNew,organizer_list=organizer_list)

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
    # print("follow User")
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
            # print('Team ALready exists')
            flash("Team name already exists for this event")
        else:
            sql_query='''
            SELECT * FROM Student WHERE student_email="{}" OR student_email="{}" OR student_email="{}" OR student_email="{}"  
            '''.format(form.member_01_email.data,form.member_02_email.data,form.member_03_email.data,form.member_04_email.data)
            try:
                # FETCHING THE TUPLES OF THE TEAM-MATES FROM THE STUDENT TABLE
                cursor.execute(sql_query)
                student_data=cursor.fetchall()
                # print(student_data)

                if len(student_data)==form.number_of_members.data:
                    # print("True")

                    #INSERING TEAM INTO THE TABLE 
                    sql_query_01='''
                    INSERT INTO Team({},{}) values(?,?)
                    '''.format("team_name","event_id")
                    try:
                        cursor.execute(sql_query_01,(form.team_name.data,eventId))
                        conn.commit()
                    except Exception as e:
                        print("Inserting into team table")
                        # print(e)

                    #FETCHING TEAM DETAILS
                    sql_query_02='''
                    SELECT * FROM Team WHERE {}="{}"
                    '''.format("team_name",form.team_name.data)
                    cursor.execute(sql_query_02)
                    team_data=cursor.fetchone()
                    # print(team_data)

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
                            # print(e)


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
            # print(student_id)
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


def funct(user_email,event_id):
    conn=db_connection()
    cursor=conn.cursor()
    sql_query='''
    SELECT * FROM Student WHERE student_email="{}" 
    '''.format(user_email)
    cursor.execute(sql_query)
    student=cursor.fetchone()
    
    sql_query='''
    SELECT * FROM Participants WHERE student_id={} AND event_id={}
    '''.format(student[0],event_id)
    cursor.execute(sql_query)
    status=cursor.fetchone()
    return status

@main.route('/eventDetailsForStudent/<int:eventId>',methods=['GET','POST'])
def eventDetailsForStudent(eventId):
    formNew=SearchUserForm()
    conn=db_connection()
    cursor=conn.cursor()

    sql_query='''
    SELECT * FROM Student WHERE student_email="{}"
    '''.format(current_user.email)

    cursor.execute(sql_query)
    visitor_id=cursor.fetchall()[0][0]
    # print(visitor_id)
    # print(eventId)
    sql_query='''
    SELECT * FROM Participants WHERE student_id={} AND event_id={}
    '''.format(visitor_id,eventId)
    # print(sql_query)
    cursor.execute(sql_query)
    data=cursor.fetchall()
    # print(datas)
    sql_query='''
    SELECT * FROM Event WHERE event_id={}
    '''.format(eventId)
    cursor.execute(sql_query)
    datas=cursor.fetchone()
    if len(data)==0:
        
        return redirect(url_for('main.eventDetailsForVoting',eventId=eventId,formNew=formNew))
    else:

        return render_template('event_details_for_student.html',datas=datas,formNew=formNew)

@main.route('/Timeline')
def Timeline():
    conn=db_connection()
    cursor =conn.cursor()
    formNew=SearchUserForm()
    userid=userDetails()[0][0]

    # SELECT * FROM Project WHERE project_id = (
    #     SELECT project_id FROM ProjectLink WHERE student_id = (
                 
    sql_query='''SELECT follower_id FROM Follow WHERE following_id = {}'''.format(userid)
    # cursor.execute(sql_query).fetchall()
    det=cursor.execute(sql_query).fetchall()
    det2=list()
    for i in det:
        # print(i)
        sql_query='''SELECT project_id FROM ProjectLink WHERE student_id ={}'''.format(i[0])
        x=cursor.execute(sql_query).fetchall()
        if x!=[]:
            sql_query='''SELECT * FROM Student WHERE student_id ={}'''.format(i[0])
            p=cursor.execute(sql_query).fetchall()
            sql_query='''SELECT * FROM Project WHERE project_id ={}'''.format(x[0][0])
            p2=cursor.execute(sql_query).fetchall()
            if p!=[] and p2!=[]:
                det2.append([p2[0],p[0]])
            # print(x)
    return render_template('log_timeline.html',formNew=formNew,det2=det2)
    


@main.route('/voteForProject/<int:team_id>/<int:student_id>/<int:event_id>')
def voteForProject(team_id,student_id,event_id):
    conn = db_connection()
    cursor = conn.cursor()
    usr_id = userDetails()[0][0]
    sql_query = '''INSERT into Votes(team_id,student_id ,event_id) values ({},{},{})'''.format(team_id,student_id,event_id)
    # print(sql_query)
    cursor =cursor.execute(sql_query)
    conn.commit()
    return redirect(url_for('main.eventDetailsForVoting',eventId=event_id))



@main.route('/eventDetailsForVoting/<int:eventId>')
def eventDetailsForVoting(eventId):
    conn=db_connection()
    cursor=conn.cursor()
    sql_query='''
    SELECT * FROM Event WHERE event_id={}
    '''.format(eventId)
    cursor.execute(sql_query)
    datas=cursor.fetchone()
  
    sql_query='''
    SELECT * FROM Team WHERE event_id = {}
    '''.format(eventId)
    cursor.execute(sql_query)
    teamdet=cursor.fetchall()
    sql_query='''
    SELECT count(team_id),student_id,team_id from Participants GROUP BY team_id HAVING event_id={}
    '''.format(eventId)
    cursor.execute(sql_query)
    req=cursor.fetchall()
    # print(req)
    # count team-leader team_id
    team_leader_name = list()
    team_name_info=list()
    team_num=list()
    for i in req:
        sql_query='''SELECT team_name from Team where team_id ={}'''.format(i[2])
        team_name_info.append(cursor.execute(sql_query).fetchall()[0][0])
        sql_query='''SELECT student_name from Student where student_id ={}'''.format(i[1])
        team_leader_name.append(cursor.execute(sql_query).fetchall()[0][0])
        team_num.append(i[0])
    print(team_name_info)
    print(team_leader_name)
    print(team_num)
    rn=len(team_leader_name)
    sql_query='''
    SELECT * FROM Student WHERE student_email="{}"
    '''.format(current_user.email)

    cursor.execute(sql_query)
    visitor_id=cursor.fetchone()[0]
    print(visitor_id)
    formNew=SearchUserForm()
    return render_template('event_details_for_voting.html',eventId=eventId,req=req,formNew=formNew,datas=datas,visitor_id=visitor_id,team_name_info=team_name_info,team_leader_name=team_leader_name,team_num=team_num,rn=rn)
