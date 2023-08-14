import os
import sys

def get_db_config():
    db_config = {
        'host' : os.getenv("CW_DB_HOST"),
        'user' : os.getenv("CW_DB_USER"),
        'password' : os.getenv("CW_DB_PASS"),
        'database'   : os.getenv("CW_DB_NAME")
    }
    
    for value in db_config:
        if value is None:
            print("ERROR: missing database environment variable(s)!")
            sys.exit()

    return db_config

def get_dir_config():
    dir_config = {
        'images' : os.getenv("CW_DIR_IMAGES"),
        'extensions' : { 'jpg', 'jpeg', 'png', 'gif' }
    }

    if dir_config['images'] is None:
        print("ERROR: missing directory environment variable(s)!")
        sys.exit()

    return dir_config

def get_env_vars():
    return (get_dir_config(), get_db_config())