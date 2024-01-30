import os
from datetime import timedelta
basedir = os.path.abspath(os.path.dirname(__file__))
ACCESS_EXPIRES = timedelta(hours=1)

class Config:
    SECRET_KEY = (
        os.environ.get("SECRET_KEY")
        or "sdjknfquiwehuirywaueijqeryyqweurruytweifjdahncduewteruwieripwqe1234567890-=#$%#$%^&*&^%^&*"
    )
    SQLAlchemy_TRACK_MODIFICATIONS = False
    JWT_SECRET_KEY = os.environ.get("JWT_SECRET_KEY") or 'sakejshueurieyhw34784ruejwrfw7457w3498293jr4iew9845y348597438i9jcijw orjifnwc uw 845uc'
    JWT_ACCESS_TOKEN_EXPIRES = ACCESS_EXPIRES

class DevConfig(Config):
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = (
        os.environ.get("DEV-DB")
        or f'sqlite:///{os.path.join(basedir, "data-dev.sqlite")}'
    )


class TestingConfig(Config):
    TESTING = True
    SQLALCHEMY_DATABASE_URI = (
        os.environ.get("TEST-DB")
        or f'sqlite:///{os.path.join(basedir, "data-test.sqlite")}'
    )


config = {"dev": DevConfig, "test": TestingConfig, "default": DevConfig}
