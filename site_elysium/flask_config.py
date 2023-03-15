class Config:
    """
    La configuration de production de Flask.
    """

    SECRET_KEY = "ChangeMeIAmNotSecure"

    # SQLAlchemy
    SQLALCHEMY_DATABASE_URI = "sqlite:///db.sqlite"


class TestConfig(Config):
    """
    La configuration de test de Flask.
    """

    TESTING = True

    # SQLAlchemy
    SQLALCHEMY_DATABASE_URI = "sqlite:///test_db.sqlite"

    # WTForms
    WTF_CSRF_ENABLED = False
