"""
Config file contains global CONSTANTS
"""
from ..utils.utils import JSONSerializable


class HostConfig:
    """
    System HOST configuration settings
    They can be changed at any time.
    """
    HOST = "0.0.0.0"
    PORT = 5000


class ServerConfig(JSONSerializable):
    """
    System configuration settings
    They can be changed at any time.
    """

    SECRET_KEY = 'my-food-service-delivery-application'


class EnvironmentConfig(ServerConfig):
    """
    System configuration settings for running environment
    They can be changed at any time.
    It extends the server config class
    """
    DEBUG = True
    TESTING = False
    ENV = "development"


class DatabaseConfig:
    """
    System configuration settings for running environment
    They can be changed at any time.
    It extends the server config class
    """
    HOST = "127.0.0.1"
    PORT = "5432"
    DATABASE = "fast-food-fast"

    SCHEMA_PRODUCTION = "public"
    #SCHEMA_TESTING = "tests"
    USER = "celestemiriams"
    PASSWORD = "lutwama@2"