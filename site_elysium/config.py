class Config:
    SECRET_KEY = "ChangeMeIAmNotSecure"
    SQLALCHEMY_DATABASE_URI = "sqlite:///db.sqlite"


class TestConfig(Config):
    TESTING = True

    SQLALCHEMY_DATABASE_URI = "sqlite:///test_db.sqlite"
