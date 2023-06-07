"""
Endpoints API lié aux rooms
"""

from flask import abort, request
from flask_login import current_user, login_required
from flask_restx import Namespace, Resource, fields
import sqlalchemy.exc

from ... import db
from ... import models as models
from ...models.schemas import question_schema, room_schema

# Type hinting
current_user: models.User

room_namespace = Namespace("Room", description="Opérations liés aux rooms", path="/")

room_model = room_namespace.model(
    "Room",
    {
        "users": fields.List(fields.Integer),
        "instructions": fields.String,
        "description": fields.String,
        "id": fields.Integer,
        "url_name": fields.String,
        "_victim_vm_ids": fields.String,
        "name": fields.String,
        "questions": fields.List(fields.Integer),
    },
)

edit_room_model = room_namespace.model(
    "EditRoom",
    {
        "instructions": fields.String,
        "description": fields.String,
        "url_name": fields.String,
        "_victim_vm_ids": fields.String,
        "name": fields.String,
    },
)


@room_namespace.route("/room/<url_name>")
@room_namespace.param("url_name", "L'url name de la room")
@room_namespace.response(200, "Succès")
@room_namespace.response(404, "La room n'existe pas")
@room_namespace.response(409, "Une room avec ce nom existe déja")
@room_namespace.response(
    422, "Une string vide a été donnée pour un champ ne le permettant pas"
)
class RoomResource(Resource):
    """Informations lié à une room"""

    @room_namespace.marshal_with(room_model, as_list=False)
    def get(self, url_name: str):
        """Récupère les informations lié a une room."""
        room: models.Room = models.Room.query.filter_by(url_name=url_name).first_or_404(
            description="Cette room n'existe pas."
        )
        return room_schema.dump(room)

    @room_namespace.expect(edit_room_model, validate=True)
    @room_namespace.marshal_with(room_model, as_list=False)
    def post(self, url_name: str):
        """Créer une nouvelle room"""
        data = request.json

        room = models.Room(
            name=data.get("name") or url_name,
            url_name=data.get("url_name") or url_name,
            description=data.get("description") or "# change me",
            instructions=data.get("instructions") or "# change me",
        )
        if data.get("_victim_vm_ids") is not None:
            room.victim_vm_ids = [
                int(i)
                for i in data.get("_victim_vm_ids", "").strip().split(";")
                if i != ""
            ]
        else:
            room.victim_vm_ids = []

        try:
            db.session.add(room)
            db.session.commit()
        except sqlalchemy.exc.IntegrityError:
            abort(409)

        return room_schema.dump(room)

    @room_namespace.expect(edit_room_model, validate=True)
    @room_namespace.marshal_with(room_model, as_list=False)
    def put(self, url_name: str):
        """Modifie une room"""
        data = request.json

        room: models.Room = models.Room.query.filter_by(url_name=url_name).first_or_404(
            description="Cette room n'existe pas."
        )

        for key in (
            "name",
            "url_name",
            "description",
            "instructions",
        ):
            if data.get(key) is None:
                continue
            if data.get(key).strip() == "":
                abort(422)
            setattr(room, key, data.get(key))
        if data.get("_victim_vm_ids") is not None:
            room.victim_vm_ids = [
                int(i)
                for i in data.get("_victim_vm_ids", "").strip().split(";")
                if i != ""
            ]

        db.session.commit()
        return room_schema.dump(room)

    def delete(self, url_name: str):
        """Supprime une room"""
        if not current_user.is_authenticated:
            abort(401)
        if not current_user.is_admin:
            abort(403)

        room: models.Room = models.Room.query.filter_by(url_name=url_name).first_or_404(
            description="Cet room n'existe pas."
        )
        db.session.delete(room)
        db.session.commit()


question_model = room_namespace.model(
    "Question",
    {
        "room": fields.Integer,
        "id": fields.Integer,
        "solved_questions_data": fields.List(
            fields.Nested(
                room_namespace.model(
                    "SolvedQuestionData",
                    {"user_id": fields.Integer, "question_id": fields.Integer},
                )
            )
        ),
        "points": fields.Integer,
        "prompt": fields.String,
    },
)


@room_namespace.route("/room/<url_name>/create_question")
@room_namespace.param("url_name", "L'url name de la room")
@room_namespace.response(200, "Succès")
@room_namespace.response(403, "L'utilisateur n'a pas les privilèges requis")
@room_namespace.response(404, "La room n'existe pas")
@room_namespace.doc(security="http")
class CreateQuestionResource(Resource):
    """Permet a un administrateur de créer une nouvelle question pour une room."""

    method_decorators = [login_required]

    @room_namespace.marshal_with(question_model, as_list=False)
    def post(self, url_name: str):
        """Permet a un administrateur de créer une nouvelle question pour une room."""
        room: models.Room = models.Room.query.filter_by(url_name=url_name).first_or_404(
            description="Cette room n'existe pas."
        )
        if not current_user.is_admin:
            abort(403)

        new_question = models.Question(
            room_id=room.id, prompt="Lorem ipsum", answer="changeme", points=2
        )
        db.session.add(new_question)

        db.session.commit()
        return question_schema.dump(new_question)


@room_namespace.route("/question/<id>")
@room_namespace.response(200, "Succès")
@room_namespace.response(401, "L'utilisateur n'est pas connecté")
@room_namespace.response(403, "L'utilisateur n'a pas les privilèges requis")
@room_namespace.response(404, "La question n'existe pas")
class QuestionResource(Resource):
    """Informations lié à une question"""

    @room_namespace.marshal_with(question_model, as_list=False)
    def get(self, id):
        """Récupère les informations lié a une question."""
        question: models.User = models.Question.query.filter_by(id=id).first_or_404(
            description="Cet question n'existe pas."
        )
        return question_schema.dump(question)

    @room_namespace.marshal_with(question_model, as_list=False)
    def put(self, id):
        """Modifie les informations lié a une question."""
        if not current_user.is_authenticated:
            abort(401)
        if not current_user.is_admin:
            abort(403)

        question: models.Question = models.Question.query.filter_by(id=id).first_or_404(
            description="Cet question n'existe pas."
        )

        data: dict = request.json
        if data.get("id"):
            del data["id"]

        for key, value in data.items():
            setattr(question, key, value)

        db.session.commit()
        return question_schema.dump(question)

    def delete(self, id):
        """Supprime une question"""
        if not current_user.is_authenticated:
            abort(401)
        if not current_user.is_admin:
            abort(403)

        question: models.User = models.Question.query.filter_by(id=id).first_or_404(
            description="Cet question n'existe pas."
        )
        db.session.delete(question)
        db.session.commit()


@room_namespace.route("/join_room/<room_url_name>")
@room_namespace.param("room_url_name", "L'url name de la room")
@room_namespace.response(200, "Succès")
@room_namespace.response(400, "L'utilisateur est déja dans la room")
@room_namespace.response(404, "La room n'existe pas")
@room_namespace.doc(security="http")
class RoomJoinResource(Resource):
    """Permet a un utilisateur de rejoindre une room."""

    method_decorators = [login_required]

    def post(self, room_url_name: str):
        """Permet a un utilisateur de rejoindre une room."""
        room: models.Room = models.Room.query.filter_by(
            url_name=room_url_name
        ).first_or_404(description="Cette room n'existe pas.")
        if current_user in room.users:
            abort(400, "L'utilisateur est deja dans la room.")
        room.users.append(current_user)
        db.session.commit()
        return {}


@room_namespace.route("/answer_question")
@room_namespace.response(200, "Succès")
@room_namespace.response(
    400,
    "Il manque un argument / L'utilisateur n'est pas dans la room / L'utilisateur a déja répondu à la question",
)
@room_namespace.doc(security="http")
class AnswerQuestionResource(Resource):
    """Permet a l'utilisateur de répondre a une question et de savoir si il a juste"""

    method_decorators = [login_required]

    @room_namespace.marshal_with(
        room_namespace.model("AnswerQuestion", {"correct": fields.Boolean})
    )
    def post(self):
        """Permet a l'utilisateur de répondre a une question et de savoir si il a juste"""
        question_id = request.args.get("question_id")
        if question_id is None:
            abort(400, "Il manque l'argument 'question_id'")

        answer = request.args.get("answer")
        if answer is None:
            abort(400, "Il manque l'argument 'answer'")

        question: models.Question = models.Question.query.filter_by(
            id=question_id
        ).first_or_404(description="Cette question n'existe pas.")
        if current_user not in question.room.users:
            abort(400, "L'utilisateur n'est pas dans la room.")

        if question.is_solved_by(current_user):
            abort(400, "L'utilisateur a déja répondu à la question.")

        answer = request.args.get("answer")
        if answer is None:
            abort(400, "Il manque l'argument 'answer'")

        if answer.casefold().strip() != question.answer.casefold().strip():
            return {"correct": False}

        question.solve(current_user)

        return {"correct": True}
