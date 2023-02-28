from datetime import datetime

from sqlalchemy import Column, DateTime, ForeignKey, Integer, String

from .. import db


class UserQuestionData(db.Model):
    """
    Stocke des informations sur la complétion d'une question par un utilisateur.
    Si une UserQuestionData existe pour une combinaison utilisateur-question, alors cet
    utilisateur à résolut cette question.
    """

    __tablename__ = "user_question_data"

    user_id = Column(Integer, ForeignKey("users.id"), primary_key=True)
    question_id = Column(Integer, ForeignKey("questions.id"), primary_key=True)

    solved_at = Column(DateTime, default=datetime.now)
