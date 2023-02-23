from __future__ import annotations
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash
from flask_login import LoginManager
from flask_admin import Admin
from typing import Optional, TYPE_CHECKING
from .backend.filters import markdown_filter

if TYPE_CHECKING:
    from .models import User


db = SQLAlchemy()
login_manager = LoginManager()
admin = Admin(name="Interface Admin", template_mode="bootstrap3")


@login_manager.user_loader
def load_user(user_id: str) -> Optional["User"]:
    from .models import User

    return User.query.filter_by(id=user_id).first()


def create_app() -> Flask:
    app = Flask(
        __name__,
        static_folder="static",
        template_folder="templates",
        static_url_path="/static",
    )
    app.config["SECRET_KEY"] = "ChangeMeIAmNotSecure"

    # SQLalchemy
    app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///db.sqlite"
    db.init_app(app)

    # flask-login
    login_manager.init_app(app)

    # flask-admin
    app.config["FLASK_ADMIN_SWATCH"] = "cerulean"
    admin.init_app(app)

    from site_elysium.models import (
        User,
        Room,
        VirtualMachine,
        Question,
        UserQuestionData,
    )
    from .classes import AdminModelView

    admin.add_view(AdminModelView(User, db.session))
    admin.add_view(AdminModelView(Room, db.session))
    admin.add_view(AdminModelView(VirtualMachine, db.session))
    admin.add_view(AdminModelView(Question, db.session))
    admin.add_view(AdminModelView(UserQuestionData, db.session))

    # Register the filters
    app.jinja_env.filters["markdown"] = markdown_filter

    # Register the blueprints
    from .routes import main, api

    app.register_blueprint(main)
    app.register_blueprint(api)

    return app


def setup_app(app: Flask):
    from site_elysium.models import Question, Room, User

    with app.app_context():
        db.create_all()

    with app.app_context():
        user = User.query.filter_by(username="admin").first()
        if user is None:
            user = User(
                username="admin",
                email="feur@desu.wa",
                password_hash=generate_password_hash("admin"),
                is_admin=True,
                score=12,
            )
            db.session.add(user)
            db.session.commit()

        room = Room.query.filter_by(id="1").first()
        if room is None:
            room = Room(
                name="Room 1",
                description="Wow what a cool room **desu wa**",
                url_name="room1",
                instructions="QCM",
                victim_vm_ids=[100],
            )
            room2 = Room(
                name="Room 2",
                description="lorem ipsum dolor sit amet",
                url_name="room2",
                instructions="QCM",
            )
            room3 = Room(
                name="Room 3",
                description="lorem ipsum dolor sit amet",
                url_name="room3",
                instructions="QCM",
            )
            room4 = Room(
                name="Room 4",
                description="lorem ipsum dolor sit amet",
                url_name="room4",
                instructions="QCM",
            )
            room5 = Room(
                name="Room 5",
                description="lorem ipsum dolor sit amet",
                url_name="room5",
                instructions="QCM",
            )
            room6 = Room(
                name="Room 6",
                description="lorem ipsum dolor sit amet",
                url_name="room6",
                instructions="QCM",
            )

            db.session.add(room)
            db.session.add(room2)
            db.session.add(room3)
            db.session.add(room4)
            db.session.add(room5)
            db.session.add(room6)

            db.session.commit()

            # room.users.append(user)
            # backend.db.session.commit()

        question = Question.query.filter_by(id="1").first()
        if question is None:
            for i in range(6):
                question = Question(room_id=1, prompt=f"{i}+1=?", answer=str(i + 1))
                db.session.add(question)
                db.session.commit()
