import pymysql

from flask import current_app, g

def create_connection():
    db_config = current_app.config['ENV_VARS']['DB']

    return pymysql.connect(
        host = db_config['host'],
        user = db_config['user'],
        password = db_config['password'],
        database = db_config['database'],
        cursorclass = pymysql.cursors.DictCursor
    )

def close_connection(c):
    print("Closing connection to DB")
    c.close()