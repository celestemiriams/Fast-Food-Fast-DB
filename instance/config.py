import os
#basedir = os.path.abspath(os.path.dirname(__file__))


class BaseConfig(object):

    """ Common configurations """

    TESTING = False
    DEBUG = False
    SECRET_KEY = 'my-food-service-delivery-application'


class TestingConfig(BaseConfig):

    """Configurations for Testing, with a separate test database."""
    if os.getenv('TRAVIS'):
        DATABASE_URL = 'postgresql://postgres@localhost:5432/postgres'
    else:
        DATABASE_URL = 'postgresql://postgres:lutwama@2@localhost:5432/postgres'
    TESTING = True
    DEBUG = True


class DevelopmentConfig(BaseConfig):
    """
    Development configurations
    """
    DATABASE_URL = 'postgresql://celestemiriams:lutwama@2@localhost:5432/fast-food-fast'
    DEBUG = True


class ProductionConfig(BaseConfig):
    """
    Production configurations
    """
    DATABASE_URL = "postgres://jgdwqdyywpxcin:fe12530756eceead021334d20dd0221d7eb4e32e2c5364b9cbbfee37dca28f20@ec2-184-72-247-70.compute-1.amazonaws.com:5432/daokvtekhjhl2s"
    DEBUG = False


app_config = {
    'development': DevelopmentConfig,
    'testing': TestingConfig,
    'production': ProductionConfig
}
