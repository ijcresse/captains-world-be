#Captain's World Server
A simple REST API to service requests for the Captain's World website. Runs on Flask.

##Installation
```
python3 -m venv .venv
. .venv/bin/activate #start venv
python3 -m pip install -r requirements.txt
#access mysql and source database setup script
>source /path/to/project/scripts/db_setup.sql
```

##Running
```
#create .env file containing the following vars
#CW_DB_HOST, CW_DB_USER, CW_DB_PASS, CW_DB_NAME
python3 -m flask --app run run
```

##Structure
react FE -> flask BE -> sql DB
captains_world/
    /views #containing static site content
    /images #containing image urls for uploaded content. db will host these image names.
    /server #containing production code for this project
