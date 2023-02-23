import pytest
from flask import Flask

from site_elysium import create_app, db
from site_elysium.config import TestConfig


@pytest.fixture()
def app():
    app = create_app(config=TestConfig)

    yield app


@pytest.fixture()
def client(app):
    return app.test_client()


@pytest.fixture()
def runner(app):
    return app.test_cli_runner()


@pytest.fixture()
def database(app: Flask):
    # On créer les tables
    with app.app_context():
        db.create_all()

    yield db

    # C'est la fin du test, on supprime les tables
    with app.app_context():
        db.drop_all()


@pytest.fixture()
def full_database(app: Flask, database):
    """BDD mais avec des données de test."""

    from site_elysium.models import User, Room, Question

    with app.app_context():
        user = User.query.filter_by(username="admin").first()
        user = User(
            username="admin",
            email="admin@root.me",
            is_admin=True,
            score=12,
        )
        user.set_password("admin")
        database.session.add(user)

        for i in range(10):
            room = Room(
                name=f"Room {i}",
                description="Wow what a cool room **desu wa**",
                url_name=f"room{i}",
                instructions=f"Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua.",
                victim_vm_ids=[100],
            )
            database.session.add(room)

        for i in range(6):
            question = Question(room_id=1, prompt=f"{i}+1=?", answer=str(i + 1))
            database.session.add(question)

        # On ajoute le tout a la base de donnée
        database.session.commit()

    return database
