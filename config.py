import os

BASE_DIR = os.path.abspath(os.path.dirname(__file__))


class Config:
	SECRET_KEY = os.environ.get('SECRET_KEY') or "ea75882e2040f75b6dc7a1b55e3ba5af1b6c19561288fb36402510d3fcce6c2b"
	MAIL_SERVER = os.environ.get('MAIL_SERVER', 'smtp.googlemail.com')
	MAIL_PORT = int(os.environ.get('MAIL_PORT', '587'))
	MAIL_USE_TLS = os.environ.get('MAIL_USE_TLS', 'true').lower() in \
	    ['true', 'on', '1']
	MAIL_USERNAME = os.environ.get('MAIL_USERNAME')
	MAIL_PASSWORD = os.environ.get('MAIL_PASSWORD')
	TALOS_MAIL_SUBJECT_PREFIX = '[Talos Social Blog]'
	TALOS_MAIL_SENDER = 'Talos Social Blog Admin <flasksocialblog.admin@example.com>'
	TALOS_ADMIN = os.environ.get('TALOS_ADMIN')
	SQLALCHEMY_TRACK_MODIFICATIONS = False

	@staticmethod
	def init_app(app):
		pass


class DevelopmentConfig(Config):
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = os.environ.get('DEV_DATABASE_URL') or \
        'sqlite:///' + os.path.join(BASE_DIR, 'data-dev.sqlite')


class TestingConfig(Config):
    TESTING = True
    SQLALCHEMY_DATABASE_URI = os.environ.get('TEST_DATABASE_URL') or \
        'sqlite://'


class ProductionConfig(Config):
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or \
        'sqlite:///' + os.path.join(BASE_DIR, 'data.sqlite')


config = {
    'development': DevelopmentConfig,
    'testing': TestingConfig,
    'production': ProductionConfig,

    'default': DevelopmentConfig
}

