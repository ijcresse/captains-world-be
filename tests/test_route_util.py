import pytest
import io
import os
from werkzeug.datastructures import FileStorage
from routes.route_util import save_image, is_authorized, session_is_active, delete_session

#save_image test suite
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

def test_it_should_reject_bad_images(client):
    assert False
    
def test_it_should_save_jpeg(app):
    test_id = 1
    test_img = FileStorage(stream = io.BytesIO(b"bytes"), filename = 'valid.png')
    with app.app_context():
        save_image(test_id, test_img)
        #cleanup
        os.remove(f"{app.config['DIR']['images']}{test_id}_{test_img.filename}")
    
def test_it_should_save_jpg(client):
    assert False
def test_it_should_save_png(client):
    assert False
def test_it_should_save_gif(client):
    assert False

#is_authorized test suite
def test_it_should_verify_authorized_users(client):
    assert False

def test_it_should_reject_unauthorized_users(client):
    assert False

def test_it_should_reject_expired_users(client):
    assert False

#session_is_active tests
def it_should_identify_new_login_times():
    assert False

def it_should_identify_expired_login_times():
    assert False

def it_should_reject_invalid_login_times():
    assert False

#delete_session tests
def it_should_delete_one_active_session():
    assert False

def it_should_do_nothing_for_inactive_sessions():
    assert False

def it_should_delete_all_active_sessions():
    assert False