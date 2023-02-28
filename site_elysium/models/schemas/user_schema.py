from marshmallow_sqlalchemy import SQLAlchemyAutoSchema, SQLAlchemySchema, auto_field

from site_elysium.models import User

# class UserSchema(SQLAlchemyAutoSchema):
#     class Meta:
#         model = User
#         include_relationships = True
#         load_instance = True


class UserSchema(SQLAlchemySchema):
    class Meta:
        model = User

    id = auto_field()
    username = auto_field()
    is_admin = auto_field()


user_schema = UserSchema()
