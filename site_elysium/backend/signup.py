from typing import Optional

import flask
import wtforms
from flask_login import LoginManager, login_required, login_user, logout_user
from flask_wtf import FlaskForm
from werkzeug.security import check_password_hash, generate_password_hash

from site_elysium.app import app
from site_elysium.backend import db
from site_elysium.models.user import User


class SignupForm(FlaskForm):
    """Formulaire de connexion"""

    username = wtforms.StringField(
        "Votre pseudo", validators=[wtforms.validators.DataRequired()]
    )
    email = wtforms.EmailField(
        "Votre adresse email", validators=[wtforms.validators.DataRequired()]
    )
    password = wtforms.PasswordField(
        "Votre mot de passe", validators=[wtforms.validators.DataRequired()]
    )
    password_confirmation = wtforms.PasswordField(
        label="Password confirm",
        validators=[
            wtforms.validators.DataRequired(),
            wtforms.validators.EqualTo(
                "password", message="Les mots de passe doivent être identique."
            ),
        ],
    )
    submit = wtforms.SubmitField("Valider")


# TODO: Support pour la méthode GET
@app.route("/inscription", methods=["POST"])
def inscription():
    form = SignupForm()
    # Si le formulaire a été correctement rempli
    if form.validate_on_submit():
        user = User(
            username=form.username.data,
            email=form.email.data,
            password_hash=generate_password_hash(form.password.data),
        )
        db.session.add(user)
        db.session.commit()

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
        return "Erreur"
        # return flask.render_template("inscription.jinja", signup_form=form)
