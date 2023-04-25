from flask import request
from flask_restx import Resource, Namespace

from ... import models as models
from ...models.schemas import room_schema, question_schema

from ... import db

# Type hinting
current_user: models.User

user_namespace = Namespace(
    "User", description="Opérations liés aux utilisateurs", path="/"
)


@user_namespace.route("/user/<username>")
class UserResource(Resource):
    """Informations lié à un utilisateur"""

    def get(self, username):
        """Récupère les informations lié a un utilisateur."""
        user: models.User = models.User.query.filter_by(username=username).first_or_404(
            description="Cet utilisateur n'existe pas."
        )
        return user_schema.dump(user)
