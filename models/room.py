from backend.db import db
from sqlalchemy import Integer, Column, String, Boolean
from . import room_user


class Room(db.Model):
    """Une room regroupant des questions et des consignes"""

    __tablename__ = "rooms"

    id = Column(Integer, primary_key=True)
    name = Column(String, unique=False, nullable=False)
    description = Column(String, nullable=False)

    users = db.relationship("User", secondary=room_user)
