from marshmallow_sqlalchemy import SQLAlchemyAutoSchema, SQLAlchemySchema, auto_field

from .. import Room


class RoomSchema(SQLAlchemyAutoSchema):
    class Meta:
        model = Room
        include_relationships = True
        load_instance = True


room_schema = RoomSchema()
