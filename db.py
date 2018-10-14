import sqlite3

db_conn = sqlite3.connect('haro.sqlite')
cursor = db_conn.cursor()
cursor.execute('''
    CREATE TABLE IF NOT EXISTS user_activity (
        id INTEGER, 
        username TEXT,
        chat_id INTEGER,
        chat_title TEXT, 
        datetime TEXT
    )
''')
db_conn.commit()
