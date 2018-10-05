"""
This module sets up the flask environment
"""

from flask import Flask
from api.views.handler import ErrorHandler
from api.routes import Urls
from api.models.database_connection import DatabaseAccess
from instance.config import app_config


def create_app(config_name):
    APP = Flask(__name__, instance_relative_config=True)
    APP.config.from_object(app_config[config_name])
    APP.config.from_pyfile('config.py')
    APP.secret_key = 'SECRET_KEY'
    APP.testing = 'TESTING'
    APP.debug = 'DEBUG'
    APP.env = 'ENVIRONMENT'
    APP.errorhandler(404)(ErrorHandler.url_not_found)
    Urls.generate_url(APP)
    DatabaseAccess.create_tables()

    return APP
