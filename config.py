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
            print("ERROR: one or more environment variables is missing!")
            sys.exit()

    return db_config

def get_env_vars():
    config = {}

    #space for additional configs
    config['DB'] = get_db_config()

    return config