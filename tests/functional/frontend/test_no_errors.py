from flask import Flask, url_for
from flask.testing import FlaskClient
from flask_sqlalchemy import SQLAlchemy
from site_elysium.models import Room


#! Cela ne teste pas l'acceuil, a fixé~
# TODO: Tester également quand authentifié
def test_routes_no_server_errors(app: Flask, client: FlaskClient):
    for rule in app.url_map.iter_rules():
        # On ne peut pas tester automatiquement les routes
        # qui ont besoin d'une variable dans l'URL
        if rule.arguments:
            continue

        r = client.get(rule.endpoint)
        # On vérifie qu'il n'y a pas d'erreur serveur
        assert not str(r.status_code).startswith("5")


def test_rooms_no_error(app: Flask, client: FlaskClient, database: SQLAlchemy):
    for room in Room.query.all():
        room: Room
        url = url_for("main.room", room_url_name=room.url_name)
        r = client.get(url)
        # On vérifie qu'il n'y a pas d'erreur
        assert r.status_code == 200
