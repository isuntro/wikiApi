import os

class Config(object):
    """Parent configuration class."""
    DEBUG = False
    CSRF_ENABLED = True
    SECRET = os.getenv('SECRET')
    DATABASE = os.path.join(os.getcwd(), 'api.db')

class DevelopmentConfig(Config):
    """Configurations for Development."""
    DEBUG = True
    
class TestingConfig(Config):
    """Configurations for Testing"""
    TESTING = True
    DATABASE = os.path.join(os.pardir, 'test.db')
    DEBUG = True

class StagingConfig(Config):
    """Configurations for Staging."""
    DEBUG = True

class ProductionConfig(Config):
    """Configurations for Production."""
    DEBUG = False
    TESTING = False

app_config = {
    'development': DevelopmentConfig,
    'testing': TestingConfig,
    'staging': StagingConfig,
    'production': ProductionConfig,
}
