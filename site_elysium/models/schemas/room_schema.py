from marshmallow_sqlalchemy import SQLAlchemyAutoSchema, SQLAlchemySchema, auto_field
<<<<<<< HEAD

=======
>>>>>>> parent of ae7853a... Tri des imports
from .. import Room


class RoomSchema(SQLAlchemyAutoSchema):
    class Meta:
        model = Room
        include_relationships = True
        load_instance = True


room_schema = RoomSchema()
