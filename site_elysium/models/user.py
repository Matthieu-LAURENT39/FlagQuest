from flask_login import UserMixin
from sqlalchemy import Boolean, Column, Integer, String
from sqlalchemy.orm import Mapped, mapped_column
from werkzeug.security import check_password_hash, generate_password_hash

from .. import db


# On hérite UserMixin afin d'avoir les @property par défaut
class User(db.Model, UserMixin):
    """Un utilisateur du site web"""

    __tablename__ = "users"

    id: Mapped[int] = mapped_column(primary_key=True)
    # collation="NOCASE" signifie que les vérification ne sont pas sensible à la case
    username: Mapped[str] = mapped_column(String(collation="NOCASE"), unique=True)
    email: Mapped[str] = mapped_column(String(collation="NOCASE"), unique=True)
    password_hash: Mapped[str]
    """
    Hash du mot de passe, de la forme 'method$salt$hash'
    Voir également https://werkzeug.palletsprojects.com/en/1.0.x/utils/#werkzeug.security.generate_password_hash
    """

    is_admin: Mapped[bool] = mapped_column(default=False)

    score: Mapped[int] = mapped_column(default=0)

    def set_password(self, password: str) -> None:
        """Défini le mot de passe d'un utilisateur en stockant son hash

        Args:
            password (str): Le nouveau mot de passe en clair de l'utilisateur
        """
        self.password_hash = generate_password_hash(password)

    def verify_password(self, password: str) -> bool:
        """Vérifie que le mot de passe soit celui de l'utilisateur

        Args:
            password (str): Le mot de passe en clair à vérifier

        Returns:
            bool: True si le mot de passe est correct, sinon False
        """
        return check_password_hash(self.password_hash, password)
