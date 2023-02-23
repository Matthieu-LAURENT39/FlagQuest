from flask import Flask
from flask_sqlalchemy import SQLAlchemy

from site_elysium.models import User


def test_user_model(database: SQLAlchemy):
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
