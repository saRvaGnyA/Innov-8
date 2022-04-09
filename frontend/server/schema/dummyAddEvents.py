import sqlite3
# def db_connection():
#     conn = None
#     try:
#         conn = sqlite3.connect("identifier.sqlite")
#     except sqlite3.error as e:
#         print(e)
#     return conn

# try:
#     
# 
conn = sqlite3.connect("identifier.sqlite")
cursor = conn.cursor()
print("correct1")
# sql_query = '''DELETE FROM ProjectTitle WHERE type_name = "Seminars";'''
sql_query = '''DELETE FROM Message;'''
# sql_query = '''DELETE FROM Sponsorship WHERE sponsor_id=1;'''
# sql_query= '''ALTER TABLE Project DROP COLUMN project_image_file'''
# sql_query= '''ALTER TABLE Event AUTO_INCREMENT = 1; '''
# sql_query = '''ALTER TABLE Event  WHERE event_id = 7;'''
# sql_query = '''UPDATE Event set event_name = "Event Name 6" where event_id = 12 '''
# sql_query = '''INSERT INTO Interest(title) values("Physics"),("Chemistry"),("Mathematics"),("Eco-friendly");'''
# sql_query = '''INSERT INTO Organizer(organizer_name,organizer) values("Science Exihibition"),("Quiz competitions"),("Seminars");'''
# sql_query= '''ALTER TABLE Project ADD COLUMN project_image_file varchar'''
# sql_query= '''UPDATE Project SET project_image_file = CAST(project_images as varchar);'''
print("correct2")
cursor.execute(sql_query)
print("correct3")
conn.commit()



# except:
#     print("Incorrect query")