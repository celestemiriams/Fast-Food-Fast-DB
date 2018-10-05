"""
This module sets up the flask emvironment
"""

from flask import Flask
from api.views.handler import ErrorHandler
from ..instance.config import EnvironmentConfig, DatabaseConfig, ServerConfig
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
