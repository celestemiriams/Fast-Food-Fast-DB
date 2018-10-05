"""
This module runs the application
"""

import os

#from api.app import create_app
from api.app import APP

# config_name = os.getenv('APP_SETTINGS') # config_name = "development"
# app = create_app(config_name)

if __name__ == '__main__':
    APP.run()