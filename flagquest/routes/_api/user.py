"""
Endpoints API lié aux utilisateurs
"""

from flask_restx import Namespace, Resource, fields

from ... import models as models
from ...models.schemas import user_schema

# Type hinting
current_user: models.User

user_namespace = Namespace(
    "User", description="Opérations liés aux utilisateurs", path="/"
)

user_model = user_namespace.model(
    "User",
    {"id": fields.Integer, "is_admin": fields.Boolean, "username": fields.String},
)


@user_namespace.route("/user/<username>")
@user_namespace.response(200, "Succès")
@user_namespace.response(404, "L'utilisateur n'existe pas")
class UserResource(Resource):
    """Informations lié à un utilisateur"""

    @user_namespace.marshal_with(user_model, as_list=False)
    def get(self, username):
        """Récupère les informations lié a un utilisateur."""
        user: models.User = models.User.query.filter_by(username=username).first_or_404(
            description="Cet utilisateur n'existe pas."
        )
        return user_schema.dump(user)
