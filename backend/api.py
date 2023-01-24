from app import app
from flask_restful import Api, Resource
from flask_login import login_required, current_user
from flask import redirect, jsonify, Blueprint, Response, abort, request
from models import User, Room, Question
import backend
from models.schemas import user_schema, room_schema
import json
import werkzeug.exceptions

api = Blueprint(
    "api",
    __name__,
    url_prefix="/api",
)
api_manager = Api(api)

# Type hinting
current_user: User


class UserResource(Resource):
    """Informations lié à un utilisateur"""

    def get(self, username):
        user: User = User.query.filter_by(username=username).first_or_404(
            description="Cet utilisateur n'existe pas."
        )
        return user_schema.dump(user)


class RoomResource(Resource):
    """Informations lié à une room"""

    def get(self, url_name: str):
        room: Room = Room.query.filter_by(url_name=url_name).first_or_404(
            description="Cette room n'existe pas."
        )
        return room_schema.dump(room)


@api.after_request
def api_after_request(r: Response) -> Response:
    """Edite toute les réponse de l'API"""
    j: dict = r.get_json()

    # Des fois il n'y a pas de data
    if isinstance(j, dict):
        # On ajoute le champ avec le succès de la requête
        j["success"] = r.status_code == 200

    r.data = json.dumps(j, indent=4)
    return r


# Formate toutes les erreurs en json
@api.errorhandler(werkzeug.exceptions.HTTPException)
def api_error_handler(error: werkzeug.exceptions.HTTPException):
    """Formatte toutes les erreurs d'API en json"""
    return {"message": error.description}, error.code


@api.route("/profile", methods=["GET"])
@login_required
def profile():
    """Redirige vers l'endpoint de l'utilisateur connecté"""
    return redirect(api_manager.url_for(UserResource, username=current_user.username))


@api.route("/join_room/<room_url_name>", methods=["POST"])
@login_required
def join_room(room_url_name: str):
    room: Room = Room.query.filter_by(url_name=room_url_name).first_or_404(
        description="Cette room n'existe pas."
    )
    if current_user in room.users:
        abort(400, "L'utilisateur est deja dans la room.")
    room.users.append(current_user)
    backend.db.session.commit()
    return {}


@api.route("/answer_question", methods=["POST"])
@login_required
def answer_question():
    question_id = request.args.get("question_id")
    if question_id is None:
        abort(400, "Il manque l'argument 'question_id'")

    answer = request.args.get("answer")
    if answer is None:
        abort(400, "Il manque l'argument 'answer'")

    question: Question = Question.query.filter_by(id=question_id).first_or_404(
        description="Cette question n'existe pas."
    )
    if current_user not in question.room.users:
        abort(400, "L'utilisateur n'est pas dans la room.")

    # TODO: vérifier si l'utilisateur à déja répondu à la question
    if question.is_solved_by(current_user):
        abort(400, "L'utilisateur a déja répondu à la question.")

    answer = request.args.get("answer")
    if answer is None:
        abort(400, "Il manque l'argument 'answer'")

    if answer.casefold().strip() != question.answer.casefold().strip():
        return {"correct": False}

    # TODO: stoqué que l'utilisateur a solve la question
    question.solve(current_user)

    return {"correct": True}


api_manager.add_resource(UserResource, "/user/<username>")
api_manager.add_resource(RoomResource, "/room/<url_name>")

app.register_blueprint(api)
