from flask.testing import FlaskClient
from flask import url_for, Flask


def test_front_page_access(client: FlaskClient):
    """
    On vérifie que la page est bien accessible et redirige bien.
    """
    front_page_request = client.get(url_for("main.acceuil"))
    assert front_page_request.status_code == 200

    # # On vérifie que la root (/) renvoie bien a la page principale
    root_request = client.get("/", follow_redirects=True)
    assert root_request.request.path == url_for("main.acceuil")


def test_all_routes_access(app: Flask, client: FlaskClient):
    """
    On vérifie que toutes les routes soient accessibles sans erreur.
    """

    def has_no_empty_params(rule):
        defaults = rule.defaults if rule.defaults is not None else ()
        arguments = rule.arguments if rule.arguments is not None else ()
        return len(defaults) >= len(arguments)

    for rule in app.url_map.iter_rules():
        # Filter out rules we can't navigate to in a browser
        # and rules that require parameters
        if "GET" in rule.methods and has_no_empty_params(rule):
            url = url_for(rule.endpoint, **(rule.defaults or {}))
            assert client.get(url).status_code in [200, 401]
