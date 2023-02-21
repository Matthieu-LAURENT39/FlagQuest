from site_elysium.backend.db import db
from sqlalchemy import Integer, Column, String, ForeignKey
from . import room_user, Room, User, UserQuestionData


class Question(db.Model):
    """Une question appartenant à une room"""

    __tablename__ = "questions"

    id = Column(Integer, primary_key=True)
    """Identifiant unique de la question. N'est pas montré à l'utilisateur."""

    room_id = Column(Integer, db.ForeignKey("rooms.id"), nullable=False)
    room: Room = db.relationship("Room", back_populates="questions")

    prompt = Column(String, nullable=False)
    """L'énoncé de la question affiché à l'utilisateur. Peut contenir du markdown."""
    answer = Column(String, nullable=False)
    """La réponse attendu à la question. Non-sensible à la case."""

    def is_solved_by(self, user: User) -> bool:
        """Vérifie si cette question a été résolu par un utilisateur.

        Args:
            user (User): L'utilisateur à vérifier.

        Returns:
            bool: True si la question a été résolue, sinon False.
        """
        user_question_data = UserQuestionData.query.filter_by(
            user_id=user.id, question_id=self.id
        ).first()

        return user_question_data is not None

    def solve(self, user: User):
        """Marque une question comme complété par un utilisateur.

        Args:
            user (User): L'utilisateur qui a résolu la question.
        """
        if not self.is_solved_by(user):
            user_question_data = UserQuestionData(user_id=user.id, question_id=self.id)
            db.session.add(user_question_data)
            db.session.commit()
