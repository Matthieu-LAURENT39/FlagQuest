from backend.db import db
from sqlalchemy import Integer, Column, String
from werkzeug.security import generate_password_hash, check_password_hash


class User(db.Model):
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
