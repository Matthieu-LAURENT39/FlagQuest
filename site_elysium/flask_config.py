class Config:
    SECRET_KEY = "ChangeMeIAmNotSecure"

    # SQLAlchemy
    SQLALCHEMY_DATABASE_URI = "sqlite:///db.sqlite"


class TestConfig(Config):
    TESTING = True

    # SQLAlchemy
    SQLALCHEMY_DATABASE_URI = "sqlite:///test_db.sqlite"

    # WTForms
    WTF_CSRF_ENABLED = False
