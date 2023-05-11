"""
Fonctions s'appliquant à tout les endpoints API
"""

import werkzeug.exceptions

from ... import models as models
from .. import api

# Type hinting
current_user: models.User


# @api.after_request
# def api_after_request(r: Response) -> Response:
#     """Edite toute les réponse de l'API"""
#     j: dict = r.get_json()

#     # Des fois il n'y a pas de data
#     if isinstance(j, dict):
#         # On ajoute le champ avec le succès de la requête
#         j["success"] = r.status_code == 200

#     r.data = json.dumps(j, indent=4)
#     return r


# Formate toutes les erreurs en json
@api.errorhandler(werkzeug.exceptions.HTTPException)
def api_error_handler(error: werkzeug.exceptions.HTTPException):
    """Formatte toutes les erreurs d'API en json"""
    return {"message": error.description}, error.code
