import pytest
import io
import os
import unittest
from unittest.mock import MagicMock
from datetime import datetime
from flask import session
from werkzeug.datastructures import FileStorage

from routes.route_util import save_image, is_authorized, session_is_active, delete_session

#save_image test suite
#i acknowledge the lack of improper image file validation. 
#the risk for bad actors is low, however
def test_it_should_not_save_other_extensions(app):
    test_id = 1
    test_empty_filename_img = {
        'filename' : '',
    }
    with app.app_context() and pytest.raises(Exception):
        save_image(test_id, test_empty_filename_img)

    test_invalid_filename_str_img = {
        'filename' : 'test.txt',
    }
    with app.app_context() and pytest.raises(Exception):
        save_image(test_id, test_invalid_filename_str_img)

    test_invalid_missing_filename_img = {
        'filename' : '.png'
    }
    with app.app_context() and pytest.raises(Exception):
        save_image(test_id, test_invalid_missing_filename_img)

    test_invalid_filename_bad_type_img = {
        'filename' : '',
    }
    with app.app_context() and pytest.raises(Exception):
        save_image(test_id, test_invalid_filename_bad_type_img)

def test_it_should_reject_wrong_format_images(app):
    test_id = 1
    test_invalid_file_type = {
        'filename' : 0,
    }
    with app.app_context() and pytest.raises(Exception):
        save_image(test_id, test_invalid_file_type)

def test_it_should_reject_bad_ids(app):
    test_bad_type_id = "1"
    test_valid_img = {
        'filename' : 'valid.png'
    }
    with app.app_context() and pytest.raises(Exception):
        save_image(test_bad_type_id, test_valid_img)

    test_impossible_id = -1
    with app.app_context() and pytest.raises(Exception):
        save_image(test_impossible_id, test_valid_img)

def test_it_should_reject_missing_images(app):
    test_id = 1
    with app.app_context and pytest.raises(Exception):
        save_image(test_id, None)
    
def test_it_should_save_jpeg(app):
    test_id = 1
    test_jpeg = FileStorage(stream = io.BytesIO(b"bytes"), filename = 'valid.jpeg')
    with app.app_context():
        save_image(test_id, test_jpeg)
        #cleanup
        os.remove(f"{app.config['DIR']['images']}{test_id}_{test_jpeg.filename}")
    
def test_it_should_save_jpg(app):
    test_id = 1
    test_jpg = FileStorage(stream = io.BytesIO(b"bytes"), filename = 'valid.jpg')
    with app.app_context():
        save_image(test_id, test_jpg)
        #cleanup
        os.remove(f"{app.config['DIR']['images']}{test_id}_{test_jpg.filename}")

def test_it_should_save_png(app):
    test_id = 1
    test_png = FileStorage(stream = io.BytesIO(b"bytes"), filename = 'valid.png')
    with app.app_context():
        save_image(test_id, test_png)
        #cleanup
        os.remove(f"{app.config['DIR']['images']}{test_id}_{test_png.filename}")

def test_it_should_save_gif(app):
    test_id = 1
    test_gif = FileStorage(stream = io.BytesIO(b"bytes"), filename = 'valid.gif')
    with app.app_context():
        save_image(test_id, test_gif)
        #cleanup
        os.remove(f"{app.config['DIR']['images']}{test_id}_{test_gif.filename}")

#is_authorized test suite
#ok it seems like i need login to be proved to have an active session to test?
def test_it_should_verify_authorized_users(client):
    c = MagicMock(name="dbconn")
    cursor = MagicMock(name="cursor")
    cursor.fetchone.return_value({'c_id': '1'})
    session_name = "cw-session"

    with client and client.session_transaction() as session:
        session[session_name] = 1
        delete_session(session_name, c)
    # with client.session_transaction() as session:
    #     session['cw-session'] = 1

    # assert is_authorized()

def test_it_should_reject_unauthorized_users(client):
    assert False

def test_it_should_reject_expired_users(client):
    assert False

#session_is_active tests
def test_it_should_identify_valid_login_times(app):
    with app.app_context():
        assert session_is_active(datetime.now())

def test_it_should_identify_expired_login_times(app):
    expired_time = datetime.strptime("01/01/00 00:00", "%d/%m/%y %H:%M")
    with app.app_context():
        assert session_is_active(expired_time) is False

#delete_session tests
def test_it_should_delete_one_active_session():
    assert False

def test_it_should_do_nothing_for_inactive_sessions():
    assert False

def test_it_should_delete_all_active_sessions():
    assert False