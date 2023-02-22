from flask.testing import FlaskClient
from flask import url_for, Flask
import pytest


def test_front_page_access(client: FlaskClient):
    """
    On vérifie que la page est bien accessible et redirige bien.
    """
    front_page_request = client.get(url_for("main.acceuil"))
    assert front_page_request.status_code == 200

    # # On vérifie que la root (/) renvoie bien a la page principale
    root_request = client.get("/", follow_redirects=True)
    assert root_request.request.path == url_for("main.acceuil")


@pytest.mark.parametrize(
    "endpoint,expected_code",
    [
        ("main.acceuil", 200),
        ("main.liste_room", 200),
        ("main.connexion", 200),
        ("main.deconnexion", 401),
    ],
)
def test_route_access(client: FlaskClient, endpoint: str, expected_code: int):
    """
    On vérifie que toutes les routes soient accessibles et ai le bon code.
    """
    url = url_for(endpoint)
    r = client.get(url, follow_redirects=True)
    assert r.status_code == expected_code
