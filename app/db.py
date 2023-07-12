import pymysql
import os
import sys

def create_connection():
    cw_host = os.getenv("CW_DB_HOST")
    cw_user = os.getenv("CW_DB_USER")
    cw_password = os.getenv("CW_DB_PASS")
    cw_database = os.getenv("CW_DB_NAME")
    
    if cw_host is None or cw_user is None or cw_password is None or cw_database is None:
        print("ERROR: one or more environment variables is missing!")
        sys.exit()

    print("Creating connection to DB")
    return pymysql.connect(
        host = cw_host,
        user = cw_user,
        password = cw_password,
        database = cw_database,
        cursorclass = pymysql.cursors.DictCursor
    )

def close_connection(c):
    print("Closing connection to DB")
    c.close()