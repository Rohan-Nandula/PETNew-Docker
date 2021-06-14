
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

class TestingConfig(Config):
    TESTING = True
