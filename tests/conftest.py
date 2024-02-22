import os
import pytest
from __init__ import create_app

@pytest.fixture()
def app():
    #setup env vars
    os.environ['CW_DB_HOST'] = 'localhost'
    os.environ['CW_DB_USER'] = 'test_user'
    os.environ['CW_DB_PASS'] = 'test_pass'
    os.environ['CW_DB_NAME'] = 'test_database'
    os.environ['CW_DB_SESSION_DURATION'] = '12:00:00'

    os.environ['CW_DIR_IMAGES'] = '/test/dir/for/images'

    os.environ['SECRET_KEY'] = 'test_secret_key'

    os.environ['CW_COOKIE_HTTPONLY'] = 'True'
    os.environ['CW_COOKIE_SECURE'] = 'False'
    os.environ['CW_COOKIE_SAMESITE'] = 'None'

    #why don't i have the images extensions set as a list? this is worth checking

    #create app instance
    app = create_app()
    app.config.update({
        "TESTING": True
    }
    )

    yield app

    #clean up

@pytest.fixture()
def client(app):
    return app.test_client()

@pytest.fixture()
def runner(app):
    return app.test_cli_runner()
