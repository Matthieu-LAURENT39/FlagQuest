from flask.testing import FlaskClient
from flask import url_for
import pytest
from enum import Enum, auto
from flask_login import login_user


def test_front_page_access(client: FlaskClient):
    """
    On vérifie que la page est bien accessible et redirige bien.
    """
    front_page_request = client.get(url_for("main.acceuil"))
    assert front_page_request.status_code == 200

    # # On vérifie que la root (/) renvoie bien a la page principale
    root_request = client.get("/", follow_redirects=True)
    assert root_request.request.path == url_for("main.acceuil")


class LoginLevel(Enum):
    NOT_LOGGED_IN = auto()
    REGULAR_USER = auto()
    ADMIN = auto()


@pytest.mark.parametrize(
    "endpoint,expected_code,login_level",
    [
        ("main.acceuil", 200, LoginLevel.NOT_LOGGED_IN),
        ("main.acceuil", 200, LoginLevel.REGULAR_USER),
        ("main.liste_room", 200, LoginLevel.NOT_LOGGED_IN),
        ("main.liste_room", 200, LoginLevel.REGULAR_USER),
        ("main.connexion", 200, LoginLevel.NOT_LOGGED_IN),
        ("main.deconnexion", 401, LoginLevel.NOT_LOGGED_IN),
        ("main.deconnexion", 200, LoginLevel.REGULAR_USER),
        ("admin.index", 403, LoginLevel.REGULAR_USER),
        ("admin.index", 200, LoginLevel.ADMIN),
        ("api.doc", 200, LoginLevel.NOT_LOGGED_IN),
        ("api.doc", 200, LoginLevel.REGULAR_USER),
        ("api.doc", 200, LoginLevel.ADMIN),
        ("main.classement", 200, LoginLevel.NOT_LOGGED_IN),
        ("main.classement", 200, LoginLevel.REGULAR_USER),
        ("main.classement", 200, LoginLevel.ADMIN),
    ],
)
def test_route_access(
    client: FlaskClient,
    endpoint: str,
    expected_code: int,
    login_level: LoginLevel,
    regular_user,
    admin_user,
):
    """
    Vérifie que toutes les routes soient accessibles et ai le bon status code.
    """
    if login_level == LoginLevel.REGULAR_USER:
        login_user(regular_user)
    elif login_level == LoginLevel.ADMIN:
        login_user(admin_user)

    url = url_for(endpoint)
    r = client.get(url, follow_redirects=True)
    assert r.status_code == expected_code
