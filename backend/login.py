import flask
from app import app
import wtforms
from flask_wtf import FlaskForm
import json
from flask_login import LoginManager, login_user, logout_user, login_required
from database.user import User
from typing import Optional
from backend import db
from werkzeug.security import generate_password_hash, check_password_hash

login_manager = LoginManager()
login_manager.init_app(app)


class LoginForm(FlaskForm):
    """Formulaire de connexion"""

    login = wtforms.StringField(
        "Login ou adresse email", validators=[wtforms.validators.DataRequired()]
    )
    password = wtforms.StringField(
        "Mot de passe", validators=[wtforms.validators.DataRequired()]
    )
    submit = wtforms.SubmitField("Valider")


@login_manager.user_loader
def load_user(user_id: str) -> Optional[User]:
    return User.query.filter_by(id=user_id).first()


@app.route("/connexion", methods=["GET", "POST"])
def connexion():
    # Here we use a class of some kind to represent and validate our
    # client-side form data. For example, WTForms is a library that will
    # handle this for us, and we use a custom LoginForm to validate.
    # if flask.request.method == "POST":
    form = LoginForm()
    # Si le formulaire a été correctement rempli
    if form.validate_on_submit():
        print("ehdciuhcuih")
        # On cherche l'utilisateur demandé
        user: User = User.query.filter_by(username=form.login.data).first()
        if user is None:
            return flask.Response("Cet utilisateur n'existe pas.", 401)

        # Vérification du hash du mot de passe
        if not check_password_hash(user.password_hash, form.password.data):
            return flask.Response("Mot de passe invalide.", 401)

        # On connecte l'utilisateur avec Flask-login (ajout des cookies de session)
        login_user(user)

        flask.flash("Logged in successfully.")

        next = flask.request.args.get("next")
        # is_safe_url should check if the url is safe for redirects.
        # See http://flask.pocoo.org/snippets/62/ for an example.
        # if not is_safe_url(next):
        #     return flask.abort(400)

        return flask.redirect(next or flask.url_for("acceuil"))
    else:
        return flask.render_template("connexion.jinja", login_form=form)


@app.route("/deconnexion")
@login_required
def deconnexion():
    logout_user()
    flask.flash("Vous avez été déconnecté.")
    return flask.redirect(flask.url_for("acceuil"))
