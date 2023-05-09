# -*- coding: utf-8 -*-
# @Author: Mattlau04
# @Date:   2023-05-04 19:21:24
# @Last Modified by:   Mattlau04
# @Last Modified time: 2023-05-09 23:43:59
"""
Modèle SQLAlchemy représentant une question d'une room
"""
from . import Room, User, SolvedQuestionData
from sqlalchemy.orm import Mapped, mapped_column, relationship

from . import _current_base, _current_relationship, _current_foreign_key
from .. import db


class Question(_current_base):
    """Une question appartenant à une room"""

    __tablename__ = "questions"

    id: Mapped[int] = mapped_column(primary_key=True)
    """Identifiant unique de la question. N'est pas montré à l'utilisateur."""

    room_id: Mapped[int] = mapped_column(_current_foreign_key("rooms.id"))
    room: Mapped[Room] = _current_relationship(back_populates="questions")

    prompt: Mapped[str]
    """L'énoncé de la question affiché à l'utilisateur. Peut contenir du markdown."""
    answer: Mapped[str]
    """La réponse attendu à la question. Non-sensible à la case."""

    points: Mapped[int]
    """
    Le nombre de points que vaut la question.
    Utilisé pour calculer le score des utilisateurs.
    """

    # Les SolvedQuestionData sont supprimer automatiquement lorsque l'on supprime une question
    solved_questions_data: Mapped[list["SolvedQuestionData"]] = relationship(
        back_populates="question", cascade="all, delete, delete-orphan"
    )

    def is_solved_by(self, user: User) -> bool:
        """Vérifie si cette question a été résolu par un utilisateur.

        Args:
            user (User): L'utilisateur à vérifier.

        Returns:
            bool: True si la question a été résolue, sinon False.
        """
        user_question_data = SolvedQuestionData.query.filter_by(
            user_id=user.id, question_id=self.id
        ).first()

        return user_question_data is not None

    def solve(self, user: User):
        """Marque une question comme complété par un utilisateur.

        Args:
            user (User): L'utilisateur qui a résolu la question.
        """
        if not self.is_solved_by(user):
            user_question_data = SolvedQuestionData(
                user_id=user.id, question_id=self.id
            )
            db.session.add(user_question_data)
            db.session.commit()
