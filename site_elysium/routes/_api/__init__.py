from flask_restful import Api

from .. import api

api_manager = Api(api)


from .all import UserResource
from .room import RoomResource, QuestionResource

api_manager.add_resource(UserResource, "/user/<username>")
api_manager.add_resource(RoomResource, "/room/<url_name>")
api_manager.add_resource(QuestionResource, "/question/<id>")
