import sqlite3

conn =sqlite3.connect("identifier.sqlite")
# conn = db_connection()
cursor = conn.cursor()
cursor = conn.execute("SELECT * FROM Student")
sql_query = """
INSERT INTO Student VALUES (
    21,"Anmdsmlnkanya", "agbaosdangera@gmail.com","bchyqgbeiucq"
);
"""

cursor.execute(sql_query)
conn.commit()
sql_query = """
INSERT INTO Student VALUES (
    2,"Ananybsakjbca", "agbanbdbefgera@gmail.com","bchyqgdnkjqabeiucq"
);
"""

cursor.execute(sql_query)
conn.commit()
sql_query = """
INSERT INTO Student VALUES (
    11,"Ananclqannya", "agbangecnklanra@gmail.com","bchyqgbeiucq"
);
"""

cursor.execute(sql_query)
conn.commit()
