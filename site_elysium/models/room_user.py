from flask import has_app_context
from sqlalchemy import Column, ForeignKey, Integer, Table

from .. import db
from . import _current_base

_table = db.Table if has_app_context() else Table
_table_args = [] if has_app_context() else [_current_base.metadata]


room_user = _table(
    "room_user",
    *_table_args,
    Column("room_id", Integer, ForeignKey("rooms.id")),
    Column("user_id", Integer, ForeignKey("users.id")),
)
"""Sert a faire une relation many to many entre Room et User"""
