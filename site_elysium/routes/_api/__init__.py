from flask_restful import Api

from .. import api

api_manager = Api(api)


from .all import RoomResource, UserResource

api_manager.add_resource(UserResource, "/user/<username>")
api_manager.add_resource(RoomResource, "/room/<url_name>")
