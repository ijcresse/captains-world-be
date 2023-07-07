#Captain's World Server
A simple REST API to service requests for the Captain's World website. Runs on Flask.

##Dependencies
python3
pip
mysql
Flask
virtualenv
flask-mysql

##Installation
```
. .venv/bin/activate #start venv
pip install -r requirements.txt
```

##Running

##Structure
react FE -> flask BE -> sql DB
captains_world/
    /views #containing static site content
    /images #containing image urls for uploaded content. db will host these image names.
    /server #containing production code for this project
