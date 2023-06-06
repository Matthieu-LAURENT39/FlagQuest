"""
Application pour le projet de BTS 2023

Développeurs:  
- Matthieu LAURENT  
- Adrien BRUAS  
- Stefen INCE
"""
from __future__ import annotations

import contextlib
import glob
from typing import TYPE_CHECKING, Optional

from flask import Flask
from flask_admin import Admin
from flask_login import LoginManager
from flask_sqlalchemy import SQLAlchemy

from .backend.filters import markdown_filter
from .flask_config import Config
from .utils import add_room_from_toml
import click

if TYPE_CHECKING:
    from .models import User


db = SQLAlchemy()
login_manager = LoginManager()


@login_manager.user_loader
def load_user(user_id: str) -> Optional["User"]:
    """Chargeur d'utilisateur pour Flask-Login

    Args:
        user_id (str): L'ID de l'utilisateur à charger.

    Returns:
        Optional[User]: L'utilisateur, ou None si il n'existe pas.
    """

    from .models import User

    return User.query.filter_by(id=user_id).first()


def create_app(config: object = Config) -> Flask:
    """App factory pour l'application Flask

    Args:
        config (object, optional): L'objet de configuration à charger. Defaults to Config.

    Returns:
        Flask: l'app Flask
    """
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
    from .classes import AdminModelView, RestrictedAdminIndexView

    # Créer l'instance va a l'encontre des principes de design des app factory, mais
    # on y est contraint du a au design de flask-admin.
    # Voir aussi https://github.com/flask-admin/flask-admin/issues/910
    admin = Admin(
        name="Interface Admin",
        template_mode="bootstrap3",
        index_view=RestrictedAdminIndexView(),
    )

    # remplacer superhero par cerulean pour screens
    app.config["FLASK_ADMIN_SWATCH"] = "cerulean"
    admin.init_app(app)

    with app.app_context():
        from .models import Question, Room, SolvedQuestionData, User, VirtualMachine

        db.create_all()

    admin.add_view(AdminModelView(User, db.session))
    admin.add_view(AdminModelView(Room, db.session))
    admin.add_view(AdminModelView(VirtualMachine, db.session))
    admin.add_view(AdminModelView(Question, db.session))
    admin.add_view(AdminModelView(SolvedQuestionData, db.session))

    # Register the filters
    app.jinja_env.filters["markdown"] = markdown_filter

    # Register the blueprints
    from .routes import api, main

    app.register_blueprint(main)
    app.register_blueprint(api)

    @app.cli.command("make-admin")
    @click.argument("username")
    def make_admin(username):
        """Donne les privilèges administrateur à un admin"""
        u = User.query.filter_by(username=username).first()
        if u is None:
            click.echo(f"L'utilisateur '{u.username}' n'existe pas", err=True)
        elif u.is_admin:
            click.echo(f"L'utilisateur '{u.username}' est déja admin", err=True)
        else:
            u.is_admin = True
            db.session.commit()
            click.echo(f"L'utilisateur '{u.username}' est maintenant admin!")

    # Enfin, on créer toutes les données
    if not app.testing:
        setup_app(app)

    # print(app.url_map)

    return app


def setup_app(app: Flask):
    """Génère des données de base dans l'app

    Args:
        app (Flask): l'app où généré les données.
    """
    from .models import Question, Room, User

    with app.app_context():
        user = User.query.filter_by(username="admin").first()
        if user is None:
            user = User(
                username="admin",
                email="feur@desu.wa",
                is_admin=True,
            )
            user.set_password("admin")
            db.session.add(user)
            db.session.commit()

        for filename in glob.glob("./rooms/*.toml"):
            with open(filename, "r", encoding="utf-8") as f:
                with contextlib.suppress(ValueError):
                    add_room_from_toml(f.read())
