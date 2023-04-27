from flask import has_app_context

# Workaround pour faire que le module soit importable
# sans un contexte flask
if has_app_context():
    from .. import db

    _current_base = db.Model
    _current_relationship = db.relationship
    _current_foreign_key = db.ForeignKey
else:
    from sqlalchemy.orm import DeclarativeBase, relationship
    from sqlalchemy import ForeignKey

    class _Base(DeclarativeBase):
        pass

    _current_base = _Base
    _current_relationship = relationship
    _current_foreign_key = ForeignKey

from .room_user import room_user
from .user_question_data import SolvedQuestionData
from .virtual_machine import VirtualMachine
from .user import User
from .room import Room
from .question import Question
