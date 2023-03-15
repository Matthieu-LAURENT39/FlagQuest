from flask import render_template
import werkzeug.exceptions
from jinja2 import TemplateNotFound

from . import main

# @app.errorhandler(404)
# def page_not_found(e: werkzeug.exceptions.NotFound):
#     print(e.__dict__)
#     # note that we set the 404 status explicitly
#     return render_template("errors/404.jinja", status_code=404), 404


@main.errorhandler(werkzeug.exceptions.HTTPException)
def generic_error(e: werkzeug.exceptions.HTTPException):
    """Gère toutes les erreurs HTTPS non géré par une autre gestionaire

    Args:
        e (werkzeug.exceptions.HTTPException): L'erreur qui a été levé
    """
    response = e.get_response()

    # On essaie d'afficher les erreurs pour lesquelles on a une page particulière
    try:
        return (
            render_template(
                f"errors/{response.status_code}.jinja", status_code=response.status_code
            ),
            response.status_code,
        )
    # Si il n'y a pas de page particulière, on affiche une page générique
    except TemplateNotFound:
        return (
            render_template(
                "errors/_base_error.jinja", status_code=response.status_code
            ),
            response.status_code,
        )
