import pymysql

from flask import current_app, g

def create_connection():

    print("Creating connection to DB")
    return pymysql.connect(
        host = current_app.config['ENV_VARS'].host,
        user = current_app.config['ENV_VARS'].user,
        password = current_app.config['ENV_VARS'].password,
        database = current_app.config['ENV_VARS'].database,
        cursorclass = pymysql.cursors.DictCursor
    )

def close_connection(c):
    print("Closing connection to DB")
    c.close()