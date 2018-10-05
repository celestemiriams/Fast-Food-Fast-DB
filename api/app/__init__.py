"""
This module sets up the flask environment
"""

from flask import Flask
from api.app.handler import ErrorHandler
from ..config.config import EnvironmentConfig, DatabaseConfig, ServerConfig
#from ..config.config import app_config
from api.routes import Urls
from api.models.database_connection import DatabaseAccess


APP = Flask(__name__)
APP.secret_key = 'SECRET_KEY'
APP.testing = 'TESTING'
APP.debug = 'DEBUG'
APP.env = 'ENVIRONMENT'
APP.errorhandler(404)(ErrorHandler.url_not_found)

Urls.generate_url(APP)
DatabaseAccess.create_tables()

# def create_app(config_name):
#     APP = Flask(__name__)
#     APP.config.from_object(app_config[config_name])
#     APP.config.from_pyfile('config.py')
#     APP.errorhandler(404)(ErrorHandler.url_not_found)
#     Urls.generate_url(APP)
#     DatabaseAccess.create_tables()

#     return APP