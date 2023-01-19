from app import app
from flask_restful import Api, Resource
from flask_login import login_required, current_user
from flask import redirect, jsonify, Blueprint
from models import User, Room
import backend
from models.schemas import user_schema

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
        user: User = User.query.filter_by(username=username).first_or_404()
        return user_schema.dump(user)


class RoomResource(Resource):
    """Informations lié à une room"""

    def get(self, room_id):
        return {"room_id": room_id}


@api.route("/profile", methods=["GET"])
@login_required
def profile():
    """Redirige vers l'endpoint de l'utilisateur connecté"""
    return redirect(api_manager.url_for(UserResource, username=current_user.username))


@api.route("/join_room/<int:room_id>", methods=["POST"])
@login_required
def join_room(room_id: int):
    room: Room = Room.query.filter_by(id=room_id).first_or_404()
    if current_user in room.users:
        return {"success": False, "error": "L'utilisateur est déja dans la room."}
    room.users.append(current_user)
    backend.db.session.commit()
    return {"success": True}


api_manager.add_resource(UserResource, "/user/<username>")
api_manager.add_resource(RoomResource, "/room/<int:room_id>")

app.register_blueprint(api)
