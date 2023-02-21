from site_elysium.app import app
from flask import render_template
import werkzeug.exceptions
from jinja2 import TemplateNotFound


# @app.errorhandler(404)
# def page_not_found(e: werkzeug.exceptions.NotFound):
#     print(e.__dict__)
#     # note that we set the 404 status explicitly
#     return render_template("errors/404.jinja", status_code=404), 404


@app.errorhandler(werkzeug.exceptions.HTTPException)
def generic_error(e: werkzeug.exceptions.HTTPException):
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
