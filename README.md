# Captain's World Server
A simple REST API to service requests for the Captain's World website. Runs on Flask.

## Installation
```
python3 -m venv .venv
. .venv/bin/activate #start venv
python3 -m pip install -r requirements.txt
#may need to install prerequisites for bcrypt. following command is for ubuntu and debian
sudo apt-get install build-essential cargo
#access mysql and source database setup script
>source /path/to/project/scripts/db_setup.sql
#create handmanaged user entries in captains_world.t_users.
```

## Running locally
```
#create .env file containing the following vars: 
#directory: CW_DIR_IMAGES
#database: CW_DB_HOST, CW_DB_USER, CW_DB_PASS, CW_DB_NAME, CW_DB_SESSION_DURATION (HH:MM:SS format)
#flask: CW_COOKIE_SECURE, CW_COOKIE_HTTPONLY, CW_COOKIE_SAMESITE
#ensure you're in the proper virtual environment
. .venv/bin/activate
#set secret runtime environment variable:
export SECRET_KEY=<snip>
python3 -m flask --app . run --debug
```

## Running Production
```
#get on deploy environment
#clone code
#set up tables with models/schema.sql
#create admin user entries
##export all environment variables into the terminal
#create secret key with a command like this
python -c 'import secrets; print(secrets.token_hex())'
#configure wsgi, add context to nginx installation
https://flask.palletsprojects.com/en/2.3.x/deploying/uwsgi/
https://www.digitalocean.com/community/tutorials/how-to-serve-flask-applications-with-uwsgi-and-nginx-on-ubuntu-22-04
https://uwsgi-docs.readthedocs.io/en/latest/Nginx.html
#the configuration should send default requests at / to the static webapp and proxy /api requests to this server.

#create .sock file, give perms to nginx
#launch the server
uwsgi --socket 127.0.0.1:5000 --wsgi-file wsgi.py --ini captains-world-be.ini
#verify /api/health can be hit and returns 200 OK
```

## Structure
```
react FE -> flask BE -> sql DB
captains_world/
    /views #containing static site content
    /images #containing image urls for uploaded content. db will host these image names.
    /server #containing production code for this project
```
