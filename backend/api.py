from app import app
from flask_restful import reqparse, abort, Api, Resource

api = Api(app)


class User(Resource):
    """Informations lié à un utilisateur"""

    def get(self, user_id):
        return {"user_id": user_id}


api.add_resource(User, "/user/<int:user_id>")
