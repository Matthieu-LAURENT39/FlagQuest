"""
Schéma Marshmallow pour les utilisateurs
"""
from marshmallow_sqlalchemy import SQLAlchemySchema, auto_field
from ...models import User


# class UserSchema(SQLAlchemyAutoSchema):
#     class Meta:
#         model = User
#         include_relationships = True
#         load_instance = True


class UserSchema(SQLAlchemySchema):
    """
    Schéma Marshmallow pour sérialisation des utilisateurs
    """

    class Meta:
        """Paramètres de configuration du schéma"""

        model = User

    id = auto_field()
    username = auto_field()
    is_admin = auto_field()


user_schema = UserSchema()
