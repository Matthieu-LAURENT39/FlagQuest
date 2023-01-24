from backend.db import db
from sqlalchemy import Integer, Column, String, ForeignKey
from . import room_user, Room


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
