from .. import db
from . import Room, User, SolvedQuestionData
from sqlalchemy.orm import Mapped, mapped_column, relationship


class Question(db.Model):
    """Une question appartenant à une room"""

    __tablename__ = "questions"

    id: Mapped[int] = mapped_column(primary_key=True)
    """Identifiant unique de la question. N'est pas montré à l'utilisateur."""

    room_id: Mapped[int] = mapped_column(db.ForeignKey("rooms.id"))
    room: Mapped[Room] = db.relationship(back_populates="questions")

    prompt: Mapped[str]
    """L'énoncé de la question affiché à l'utilisateur. Peut contenir du markdown."""
    answer: Mapped[str]
    """La réponse attendu à la question. Non-sensible à la case."""

    points: Mapped[int]
    """
    Le nombre de points que vaut la question.
    Utilisé pour calculer le score des utilisateurs.
    """

    solved_questions_data: Mapped[list["SolvedQuestionData"]] = relationship(
        back_populates="question"
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
