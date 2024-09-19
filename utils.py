import sqlite3
import os

basedir = os.path.abspath(os.path.dirname(__file__))


#Connect to the DB
def get_database_connection():
    try:
        conn = sqlite3.connect('D://PROJECT//API//violation.db')
        return conn
    except Exception as e:
        print(f"Error connecting to database: {e}")
        return 
