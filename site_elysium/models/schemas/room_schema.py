from marshmallow_sqlalchemy import SQLAlchemyAutoSchema
from .. import Room


class RoomSchema(SQLAlchemyAutoSchema):
    """
    Schéma Marshmallow pour sérialisation des rooms
    """

    class Meta:
        """Paramètres de configuration du schéma"""
        model = Room
        include_relationships = True
        load_instance = True


room_schema = RoomSchema()
