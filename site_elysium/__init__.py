from __future__ import annotations
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_admin import Admin
from .backend.filters import markdown_filter
from .flask_config import Config

from typing import Optional, TYPE_CHECKING

if TYPE_CHECKING:
    from .models import User


db = SQLAlchemy()
login_manager = LoginManager()


@login_manager.user_loader
def load_user(user_id: str) -> Optional["User"]:
    from .models import User

    return User.query.filter_by(id=user_id).first()


def create_app(config: object = Config) -> Flask:
    app = Flask(
        __name__,
        static_folder="static",
        template_folder="templates",
        static_url_path="/static",
    )

    # On charge les constantes
    app.config.from_pyfile("app_config.py")

    # Puis on charge la config flask
    app.config.from_object(config)

    # SQLalchemy
    db.init_app(app)

    # flask-login
    login_manager.init_app(app)

    # flask-admin
    # Créer l'instance va a l'encontre des principes de design des app factory, mais
    # on y est contraint du a au design de flask-admin.
    # Voir aussi https://github.com/flask-admin/flask-admin/issues/910
    admin = Admin(name="Interface Admin", template_mode="bootstrap3")

    app.config["FLASK_ADMIN_SWATCH"] = "cerulean"
    admin.init_app(app)

    from site_elysium.models import (
        Question,
        Room,
        User,
        UserQuestionData,
        VirtualMachine,
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

    # Enfin, on créer toutes les données
    if not app.testing:
        setup_app(app)

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
                is_admin=True,
                score=12,
            )
            user.set_password("admin")
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
            question = Question(
                room_id=1,
                prompt="""**Qui** a écrit *cette* __question__?
Indice: `matt`
Et voici un code block
```py
import random
n = random.randint(1,10)
print(n)
```""",
                answer="matt",
            )
            db.session.add(question)
            for i in range(6):
                question = Question(room_id=1, prompt=f"{i}+1=?", answer=str(i + 1))
                db.session.add(question)
                db.session.commit()
