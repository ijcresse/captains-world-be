import os
import sys

def get_db_config():
    db_config = {
        'host' : os.getenv("CW_DB_HOST"),
        'user' : os.getenv("CW_DB_USER"),
        'password' : os.getenv("CW_DB_PASS"),
        'database'   : os.getenv("CW_DB_NAME"),
        'session_timeout' : os.getenv("CW_DB_SESSION_DURATION")
    }
    
    for value in db_config:
        if db_config[value] is None:
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

def get_secret_config():
    secret_config = {
        'key' : os.environ.get("SECRET_KEY"),
    }
    for value in secret_config:
        if secret_config[value] is None:
            print("ERROR: missing secret environment variable(s)!")
            sys.exit()

    return secret_config

def get_flask_config():
    flask_config = {
        'cookie_httponly' : os.getenv('CW_COOKIE_HTTPONLY'),
        'cookie_secure' : os.getenv('CW_COOKIE_SECURE'),
        'cookie_samesite' : os.getenv('CW_COOKIE_SAMESITE')
    }

    for value in flask_config:
        if flask_config[value] is None:
            print("ERROR: missing flask configuration env vars!")
            sys.exit()
    return flask_config

def get_env_vars():
    return (get_dir_config(), get_db_config(), get_secret_config(), get_flask_config())