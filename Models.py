import sqlite3
import os


db_connect = sqlite3.connect(os.getcwd() + '/QZJW.db')
db_cursor = db_connect.cursor()

db_cursor.execute('''
CREATE TABLE jwxt_result(
    kcmc TEXT NOT NULL,
    zcj REAL NOT NULL)
''')

db_cursor.execute('''
CREATE TABLE jwxt_token(
    id INT PRIMARY KEY NOT NULL,
    token TEXT NOT NULL)
''')

db_connect.commit()
