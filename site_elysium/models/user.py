from site_elysium.backend.db import db
from sqlalchemy import Integer, Column, String, Boolean
from flask_login import UserMixin

# On hérite UserMixin afin d'avoir les @property par défaut
class User(db.Model, UserMixin):
    """Un utilisateur du site web"""

    __tablename__ = "users"

    id = Column(Integer, primary_key=True)
    username = Column(String, unique=True, nullable=False)
    email = Column(String, unique=True, nullable=False)
    password_hash = Column(String, unique=True, nullable=False)
    """
    Hash du mot de passe, de la forme 'method$salt$hash'
    Voir également https://werkzeug.palletsprojects.com/en/1.0.x/utils/#werkzeug.security.generate_password_hash
    """

    is_admin = Column(Boolean, nullable=False, default=False)

    score = Column(Integer, nullable=False, default=0)
