from site_elysium.backend.db import db
from sqlalchemy import Integer, Column, String, ForeignKey, DateTime
from datetime import datetime


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
