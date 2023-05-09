# -*- coding: utf-8 -*-
# @Author: Mattlau04
# @Date:   2023-05-04 19:21:24
# @Last Modified by:   Mattlau04
# @Last Modified time: 2023-05-09 23:45:41
"""
Modèle SQLAlchemy représentant un utilisateur
"""
from __future__ import annotations

from flask_login import UserMixin
from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column, relationship
from werkzeug.security import check_password_hash, generate_password_hash
import datetime
from typing import TYPE_CHECKING
from functools import lru_cache
import customidenticon


from . import room_user, SolvedQuestionData
from . import _current_base


if TYPE_CHECKING:
    from . import Room


# On hérite UserMixin afin d'avoir les @property par défaut
class User(db.Model):
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

    solved_questions_data: Mapped[list["SolvedQuestionData"]] = relationship(
        back_populates="user", cascade="all, delete, delete-orphan"
    )
    joined_rooms: Mapped[list["Room"]] = relationship(
        secondary=room_user, back_populates="users"
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
        """Calcule le nombre de points que l'utilisateur avais a une certaine date

        Args:
            date (datetime.date): La date pour laquelle calculer

        Raises:
            ValueError: La date est dans le futur

        Returns:
            int: Le nombre de points
        """
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
        """Le nombre de points que possède l'utilisateur"""
        return self.points_at_date(datetime.date.today())

    @lru_cache(maxsize=5)
    def get_profile_picture(self, size: int = 250) -> bytes:
        """Gets the profile picture of a user as an image.

        Args:
            size (int, optional): The size of the square, in pixels. Defaults to 250.

        Returns:
            bytes: A PNG image.
        """
        return customidenticon.create(
            self.username.casefold(),  # Data used to generate identicon
            type="pixels",
            format="png",
            background="#f0f0f0",
            block_visibility=255,
            block_size=size // 10,  # size of elements (px)
            border=25,  # border (px)
            size=10,  # number of elements
        )
