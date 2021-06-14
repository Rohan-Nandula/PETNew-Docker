
class Config(object):
    DEBUG = False
    TESTING = False
    SECRET_KEY = 'AgeisJustanumber#Balufightsthishardway#Pythonway'
    SQLALCHEMY_DATABASE_URI = 'sqlite:///db.qlite3'
	SQLALCHEMY_TRACK_MODIFICATIONS = False

class ProductionConfig(Config):
    DATABASE_URI = 'mysql://user@localhost/foo'


class DevelopmentConfig(Config):
    DEBUG = True
    Domain=www.personalexpensetracker.com
    JWT_SECRET_KEY=Special#Keys#Require#JWT2021
    JWT_BLACKLIST_ENABLED=True
    JWT_BLACKLIST_TOKEN_CHECKS=['access', 'refresh']
    MAX_CONTENT_LENGTH=16 * 1000 * 1000

class TestingConfig(Config):
    TESTING = True
