import flask
from app import app
import wtforms
from flask_wtf import FlaskForm
import json
from flask_login import LoginManager, login_user
from database.user import User
from backend import db

login_manager = LoginManager()
login_manager.init_app(app)


class LoginForm(FlaskForm):
    """Formulaire de connection"""

    login = wtforms.StringField("login", validators=[wtforms.validators.DataRequired()])
    """Username OU email"""
    password = wtforms.StringField(
        "Email Address", validators=[wtforms.validators.DataRequired()]
    )


@login_manager.user_loader
def load_user(user_id: str):
    return User.query.filter_by(id=user_id).first()


@app.route("/login", methods=["POST"])
def login():
    # Here we use a class of some kind to represent and validate our
    # client-side form data. For example, WTForms is a library that will
    # handle this for us, and we use a custom LoginForm to validate.
    # if flask.request.method == "POST":
    form = LoginForm()
    # Si le formulaire a été correctement rempli
    if form.validate():
        # On cherche l'utilisateur demandé
        user = User.query.filter_by(username=form.login).first()

        # user should be an instance of your `User` class
        login_user(user)

        flask.flash("Logged in successfully.")

        next = flask.request.args.get("next")
        # is_safe_url should check if the url is safe for redirects.
        # See http://flask.pocoo.org/snippets/62/ for an example.
        # if not is_safe_url(next):
        #     return flask.abort(400)

        return flask.redirect(next or flask.url_for("/"))
    else:
        return json.dumps(form.errors)
