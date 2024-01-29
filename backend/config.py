import os

basedir = os.path.abspath(os.path.dirname(__file__))


class Config:
    SECRET_KEY = (
        os.environ.get("SECRET_KEY")
        or "sdjknfquiwehuirywaueijqeryyqweurruytweifjdahncduewteruwieripwqe1234567890-=#$%#$%^&*&^%^&*"
    )
    SQLAlchemy_TRACK_MODIFICATIONS = False


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
