from sqlalchemy import Column, ForeignKey, Integer

from .. import db

room_user = db.Table(
    "room_user",
    Column("room_id", Integer, ForeignKey("rooms.id")),
    Column("user_id", Integer, ForeignKey("users.id")),
)
"""Sert a faire une relation many to many entre Room et User"""
