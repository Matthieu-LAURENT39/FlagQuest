"""
Fichier de configuration de Flask
"""


class Config:
    """
    La configuration de production de Flask.
    """

    SECRET_KEY = "ChangeMeIAmNotSecure"

    # SQLAlchemy
    SQLALCHEMY_DATABASE_URI = "sqlite:///db.sqlite"
    # Exemple de l'utilisation d'une base de donnée distante
    # SQLALCHEMY_DATABASE_URI = (
    #     "mysql+pymysql://FlagQuest:passw0rd@172.17.50.250:3306/flagquest"
    # )


class TestConfig(Config):
    """
    La configuration de test de Flask.
    """

    TESTING = True

    # SQLAlchemy
    SQLALCHEMY_DATABASE_URI = "sqlite:///test_db.sqlite"

    # WTForms
    WTF_CSRF_ENABLED = False
