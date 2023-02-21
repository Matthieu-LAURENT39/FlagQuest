from flask.testing import FlaskClient
from flask import url_for


def test_front_page_access(client: FlaskClient):
    """
    On vérifie que la page est bien accessible.
    """
    front_page_request = client.get(url_for("acceuil"))
    assert front_page_request.status_code == 200

    # # On vérifie que la root (/) renvoie bien a la page principale
    root_request = client.get("/", follow_redirects=True)
    assert root_request.request.path == url_for("acceuil")
