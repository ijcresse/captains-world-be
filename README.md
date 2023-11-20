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
#flask: FLASK_SESSION_COOKIE_SECURE, FLASK_SESSION_COOKIE_HTTPONLY
#ensure you're in the proper virtual environment
. .venv/bin/activate
#set secret runtime environment variable:
export SECRET_KEY=<snip>
python3 -m flask --app . run --debug
```

## Building for Production
```
#get on deploy environment
#clone code
#export all environment variables into the terminal
#configure wsgi, add context to nginx installation
https://www.digitalocean.com/community/tutorials/how-to-serve-flask-applications-with-uwsgi-and-nginx-on-ubuntu-22-04
https://uwsgi-docs.readthedocs.io/en/latest/Nginx.html
#verify /api/health can be hit and returns 200 OK
```

## Running in Production
```

```

## Structure
react FE -> flask BE -> sql DB
captains_world/
    /views #containing static site content
    /images #containing image urls for uploaded content. db will host these image names.
    /server #containing production code for this project

### cors and cookie note
this is mostly a note for myself so i don't have to dig around.
in order to send cookies across https from webapp origin to server origin:
httponly: false
secure: true
samesite: none