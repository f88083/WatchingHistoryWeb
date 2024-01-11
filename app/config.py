import os
import sys

# SQLite URI compatible
WIN = sys.platform.startswith('win')
if WIN:
    prefix = 'sqlite:///'
else:
    prefix = 'sqlite:////'

def create_sqlite_uri(db_name):
    return prefix + os.path.join(os.path.dirname(__file__), os.getenv('DATABASE_FILE', db_name))

class BaseConfig(object):
    SECRET_KEY = os.getenv('SECRET_KEY', 'dev')

class DevelopmentConfig(BaseConfig):
    DEBUG = False
    SQLALCHEMY_DATABASE_URI = create_sqlite_uri('watching-history-dev.db')
    SQLALCHEMY_TRACK_MODIFICATIONS = False

class ProductionConfig(BaseConfig):
    DEBUG = False
    SQLALCHEMY_DATABASE_URI = create_sqlite_uri('watching-history.db')
    SQLALCHEMY_TRACK_MODIFICATIONS = False

class TestingConfig(BaseConfig):
    TESTING = True
    SQLALCHEMY_DATABASE_URI = create_sqlite_uri('test.db')
    SQLALCHEMY_TRACK_MODIFICATIONS = False

config = {
    'development': DevelopmentConfig,
    'production': ProductionConfig,
    'testing': TestingConfig
}