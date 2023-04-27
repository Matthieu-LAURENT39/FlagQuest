import json

import werkzeug.exceptions
from flask import Blueprint, Response, abort, jsonify, redirect, request, current_app
from flask_login import current_user, login_required
from flask_restful import Api, Resource

from ... import models as models
from ...models import VirtualMachine, Room
from ...models.schemas import room_schema, question_schema

from ... import db
from .. import api

# Type hinting
current_user: models.User


class RoomResource(Resource):
    """Informations lié à une room"""

    def get(self, url_name: str):
        """Récupère les informations lié a une room."""
        room: models.Room = models.Room.query.filter_by(url_name=url_name).first_or_404(
            description="Cette room n'existe pas."
        )
        return room_schema.dump(room)


class QuestionResource(Resource):
    """Informations lié à une question"""

    def get(self, id):
        """Récupère les informations lié a une Room."""
        question: models.User = models.Question.query.filter_by(id=id).first_or_404(
            description="Cet question n'existe pas."
        )
        return question_schema.dump(question)

    def post(self, id):
        """Récupère les informations lié a une Room."""
        question: models.User = models.Question.query.filter_by(id=id).first_or_404(
            description="Cet question n'existe pas."
        )

        data: dict = request.json
        if data.get("id"):
            del data["id"]

        for key, value in data.items():
            setattr(question, key, value)

        db.session.commit()
        return question_schema.dump(question)
