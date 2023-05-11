from flask import Flask
from flask_sqlalchemy import SQLAlchemy


def test_user_model(app, database: SQLAlchemy):
    with app.app_context():
        from flagquest.models import User

    user = User(username="MyTestUser", email="testuser@test.com")
    user.set_password("123456")
    database.session.add(user)
    database.session.commit()

    stored_user = User.query.filter_by(username="MyTestUser").first()
    # On vérifie que les données soient bien stoqué
    assert stored_user.email == "testuser@test.com"
    assert stored_user.verify_password("123456")

    # On vérifie que le mot de passe ne soit pas stoqué en clair
    assert stored_user.password_hash != "123456"


def test_room_model(app, database: SQLAlchemy):
    with app.app_context():
        from flagquest.models import Room

        test_room = Room(
            name="test_room_model",
            url_name="test_room_model",
            description="",
            instructions="",
        )
        assert test_room.victim_vm_ids == []

        database.session.add(test_room)
        database.session.flush()
        assert test_room.victim_vm_ids == []

        test_room.victim_vm_ids += [123]
        database.session.flush()
        assert test_room.victim_vm_ids == [123]

        test_room.victim_vm_ids += [12, 14]
        database.session.flush()
        assert test_room.victim_vm_ids == [123, 12, 14]
