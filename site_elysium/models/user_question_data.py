from __future__ import annotations

from . import _current_base
from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship
from datetime import datetime
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from . import User, Question


class SolvedQuestionData(_current_base):
    """
    Stocke des informations sur la complétion d'une question par un utilisateur.
    Si une SolvedQuestionData existe pour une combinaison utilisateur-question, alors cet
    utilisateur à résolut cette question.
    """

    __tablename__ = "user_question_data"

    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"), primary_key=True)
    question_id: Mapped[int] = mapped_column(
        ForeignKey("questions.id"), primary_key=True
    )

    user: Mapped["User"] = relationship(back_populates="solved_questions_data")
    question: Mapped["Question"] = relationship(back_populates="solved_questions_data")

    solved_at: Mapped[datetime] = mapped_column(default=datetime.now)
