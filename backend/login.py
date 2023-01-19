from typing import Optional

import flask
import wtforms
from flask_login import LoginManager, login_required, login_user, logout_user
from flask_wtf import FlaskForm
from werkzeug.security import check_password_hash, generate_password_hash

from app import app
from backend import db
from database.user import User

login_manager = LoginManager()
login_manager.init_app(app)


class LoginForm(FlaskForm):
    """Formulaire de connexion"""

    login = wtforms.StringField(
        "Login ou adresse email", validators=[wtforms.validators.DataRequired()]
    )
    password = wtforms.PasswordField(
        "Mot de passe", validators=[wtforms.validators.DataRequired()]
    )
    submit = wtforms.SubmitField("Valider")


@login_manager.user_loader
def load_user(user_id: str) -> Optional[User]:
    return User.query.filter_by(id=user_id).first()


@app.route("/connexion", methods=["GET", "POST"])
def connexion():
    form = LoginForm()
    # Si le formulaire a été correctement rempli
    if form.validate_on_submit():
        # On cherche l'utilisateur demandé
        user: User = User.query.filter_by(username=form.login.data).first()
        if user is None:
            form.login.errors.append("Cet utilisateur n'existe pas.")

        # Vérification du hash du mot de passe
        elif not check_password_hash(user.password_hash, form.password.data):
            form.password.errors.append("Mot de passe invalide.")

        # Pas d'erreur, on connecte l'utilisateur avec Flask-login (ajout des cookies de session)
        else:
            login_user(user)

            flask.flash("Logged in successfully.")

            next = flask.request.args.get("next")
            # is_safe_url should check if the url is safe for redirects.
            # See http://flask.pocoo.org/snippets/62/ for an example.
            # if not is_safe_url(next):
            #     return flask.abort(400)

            # On redirige vers la page d'acceuil
            return flask.redirect(next or flask.url_for("acceuil"))

    # Si on a pas submit une form valide, ou alors que l'on avais
    # un MDP invalide ou un login qui n'existait pas
    return flask.render_template("connexion.jinja", login_form=form)


@app.route("/deconnexion")
@login_required
def deconnexion():
    logout_user()
    flask.flash("Vous avez été déconnecté.")
    return flask.redirect(flask.url_for("acceuil"))
