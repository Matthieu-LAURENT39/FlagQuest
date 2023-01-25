from backend.db import db
from sqlalchemy import Integer, Column, String, Boolean
from . import room_user


class Room(db.Model):
    """Une room regroupant des questions et des consignes"""

    __tablename__ = "rooms"

    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    """Le nom qui est affiché à l'utilisateur"""
    url_name = Column(String, unique=True, nullable=False)
    """Le nom utilisé dans les URLs"""

    description = Column(String, nullable=False)
    """Une courte description de la room. Utilisé en dehors de la room afin d'expliquer son sujet."""

    instructions = Column(String, nullable=False)
    """Les consignes de la room, affiché au dessus des questions. Peut contenir du markdown."""

    users = db.relationship("User", secondary=room_user)

    questions = db.relationship("Question", back_populates="room")
