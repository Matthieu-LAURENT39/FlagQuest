from flask_restx import Api, Namespace

from .. import api

api_manager = Api(
    version="1.0",
    title="RootMe",
    description="L'API du site Root Me d'Elysium",
    endpoint="/api",
)


from . import all
from .room import room_namespace
from .user import user_namespace
from .vm import vm_namespace

api_manager.add_namespace(room_namespace)
api_manager.add_namespace(user_namespace)
api_manager.add_namespace(vm_namespace)

api_manager.init_app(api)
