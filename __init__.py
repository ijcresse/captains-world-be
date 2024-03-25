from datetime import datetime

from flask import Flask
from flask.logging import default_handler
import logging
from logging.config import dictConfig

from services import db
from routes.health import health_api
from routes.drinks import drinks_api
from routes.users import users_api
from routes.tags import tags_api
from routes.search import search_api
from config import get_env_vars

dictConfig({
        "version": 1,
        "formatters": {
            "default": {
                "format": "[%(asctime)s] %(levelname)s in %(module)s: %(message)s",
            }
        },
        "handlers": {
            "console": {
                "class": "logging.StreamHandler",
                "stream": "ext://sys.stdout",
                "formatter": "default",
            },
            "file": {
                "class": "logging.FileHandler",
                "filename": "cw-be.log",
                "formatter": "default",
            },
            "size-rotate": {
                "class": "logging.handlers.RotatingFileHandler",
                "filename": "cw-be.log",
                "maxBytes": 1000000,
                "backupCount": 5,
                "formatter": "default",
            },
        },
        "root": {"level": "DEBUG", "handlers": ["console", "file"]},
})

def create_app():
    app = Flask(__name__)
    app.logger.removeHandler(default_handler)
    #allow captain's world webapp to hit server - designed to run on same host
    
    cw_dir, cw_db, cw_secret, cw_flask = get_env_vars()
    app.config['DIR'] = cw_dir
    app.config['DB'] = cw_db
    app.secret_key = cw_secret['key']
    app.config.update(
        SESSION_COOKIE_HTTPONLY = cw_flask['cookie_httponly'],
        SESSION_COOKIE_SECURE = cw_flask['cookie_secure'],
        SESSION_COOKIE_SAMESITE = cw_flask['cookie_samesite']
    )

    logging.info(f"Starting Captain's World Backend Server at {datetime.now()}")
    logging.info(f"Debug Mode: {app.config['DEBUG']}")
    logging.info(f"Image dir set to: {app.config['DIR']['images']}")
    logging.info(f"Image extensions allowed set to: {app.config['DIR']['extensions']}")
    logging.info(f"Session Cookie HTTP Only: {app.config['SESSION_COOKIE_HTTPONLY']}")
    logging.info(f"Session Cookie Secure: {app.config['SESSION_COOKIE_SECURE']}")
    logging.info(f"Session Cookie Same Site: {app.config['SESSION_COOKIE_SAMESITE']}")
    logging.info(f"Secret Key set: {app.secret_key is not None}")
    
    app.register_blueprint(health_api)
    app.register_blueprint(drinks_api)
    app.register_blueprint(users_api)
    app.register_blueprint(tags_api)
    app.register_blueprint(search_api)

    db.init_app(app)

    return app
