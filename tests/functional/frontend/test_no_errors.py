from flask import Flask, url_for
from flask.testing import FlaskClient
from flask_sqlalchemy import SQLAlchemy
import pytest
from flask_login import login_user


# TODO: Tester également quand authentifié
@pytest.mark.parametrize("user", (None, "regular_user", "admin_user"))
def test_routes_no_server_errors(
    app: Flask, client: FlaskClient, user: str | None, request
):
    if user is not None:
        user_obj = request.getfixturevalue(user)
        login_user(user_obj)

    for rule in app.url_map.iter_rules():
        # On ne peut pas tester automatiquement les routes
        # qui ont besoin d'une variable dans l'URL
        if rule.arguments:
            continue

        r = client.get(rule.endpoint)
        # On vérifie qu'il n'y a pas d'erreur serveur
        assert not str(r.status_code).startswith("5")


@pytest.mark.parametrize("user", (None, "regular_user", "admin_user"))
def test_rooms_no_error(app: Flask, client: FlaskClient, user: str | None, request):
    with app.app_context():
        from flagquest.models import Room

        if user is not None:
            user_obj = request.getfixturevalue(user)
            login_user(user_obj)

    for room in Room.query.all():
        room: Room
        url = url_for("main.room", room_url_name=room.url_name)
        r = client.get(url)
        # On vérifie qu'il n'y a pas d'erreur
        assert r.status_code == 200
