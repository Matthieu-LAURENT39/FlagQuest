"""
Schéma Marshmallow pour les questions
"""
from marshmallow_sqlalchemy import SQLAlchemyAutoSchema
from .. import Question


class QuestionSchema(SQLAlchemyAutoSchema):
    """
    Schéma Marshmallow pour sérialisation des questions
    """

    class Meta:
        """Paramètres de configuration du schéma"""

        model = Question
        include_relationships = True
        load_instance = True


question_schema = QuestionSchema()
