import os
import sys

def get_db_config():
    db_config = {
        'host' : os.getenv("CW_DB_HOST"),
        'user' : os.getenv("CW_DB_USER"),
        'password' : os.getenv("CW_DB_PASS"),
        'database'   : os.getenv("CW_DB_NAME")
    }
    
    config_missing = False
    for value in db_config:
        if value is None:
            config_missing = True
            break
    
    if config_missing:
        print("ERROR: one or more environment variables is missing!")
        sys.exit()
    else:
        return db_config

def get_env_vars():
    config = {}

    config['DB'] = get_db_config()

    return config