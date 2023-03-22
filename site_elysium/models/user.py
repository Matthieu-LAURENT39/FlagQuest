from __future__ import annotations

from flask_login import UserMixin
from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column, relationship
from werkzeug.security import check_password_hash, generate_password_hash
import datetime
from typing import TYPE_CHECKING
from functools import lru_cache

from . import room_user, SolvedQuestionData
from .. import db

if TYPE_CHECKING:
    from . import Room, Question


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

    joined_rooms: Mapped[list["Room"]] = relationship(
        secondary=room_user, back_populates="users"
    )
    solved_questions_data: Mapped[list["SolvedQuestionData"]] = relationship(
        back_populates="user"
    )

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

    # On n'affiche jamais plus d'un ans de données, donc
    # on limite le cache à 366 jours
    @lru_cache(maxsize=366)
    def points_at_date(self, date: datetime.date) -> int:
        if datetime.date.today() < date:
            # The date is strictly into the future
            raise ValueError("Date is into the future.")

        # Pour chaque question résolu par l'utilisateur, on
        # ajoute la valeur en point si et seulement si
        # la question a été résolu avant la date spécifié.
        return sum(
            q.question.points
            for q in self.solved_questions_data
            if q.solved_at.date() <= date
        )

    @property
    def score(self) -> int:
        return self.points_at_date(datetime.date.today())
