from flask import flash, redirect, render_template, request, url_for
from flask_login import login_required, login_user, logout_user

from ...forms import LoginForm, SignupForm
from ...models import User

from ... import db
from . import main


@main.route("/connexion", methods=["GET", "POST"])
def connexion():
    """Formulaire permettant la connexion."""
    form = LoginForm()
    # Si le formulaire a été correctement rempli
    if form.validate_on_submit():
        # On cherche l'utilisateur demandé
        user: User = User.query.filter_by(username=form.login.data).first()
        if user is None:
            form.login.errors.append("Cet utilisateur n'existe pas.")
            flash("user inexistant", "error")

        # Vérification du hash du mot de passe
        elif not user.verify_password(form.password.data):
            form.password.errors.append("Mot de passe invalide.")

        # Pas d'erreur, on connecte l'utilisateur avec Flask-login (ajout des cookies de session)
        else:
            login_user(user)

            flash("Logged in successfully.", "success")

            next_url = request.args.get("next")
            # is_safe_url should check if the url is safe for redirects.
            # See http://flask.pocoo.org/snippets/62/ for an example.
            # if not is_safe_url(next):
            #     return flask.abort(400)

            # On redirige vers la page d'acceuil
            return redirect(next_url or url_for("main.acceuil"))

    # Si on a pas submit une form valide, ou alors que l'on avais
    # un MDP invalide ou un login qui n'existait pas
    return render_template("connexion.jinja", login_form=form)


@main.route("/deconnexion")
@login_required
def deconnexion():
    """Déconnecte automatiquement les utilisateurs."""
    logout_user()
    flash("Vous avez été déconnecté.", "info")
    return redirect(url_for("main.acceuil"))


# TODO: Support pour la méthode GET
@main.route("/inscription", methods=["POST"])
def inscription():
    """Formulaire permettant l'inscription"""
    form = SignupForm()
    # Si le formulaire a été correctement rempli
    if form.validate_on_submit():
        user = User(
            username=form.username.data,
            email=form.email.data,
        )
        user.set_password(form.password.data)

        # ajouter l'utilisateur
        db.session.add(user)
        # enregistrer la modification
        db.session.commit()

        # On connecte l'utilisateur avec Flask-login (ajout des cookies de session)
        login_user(user)

        flash("Logged in successfully.")

        next_url = request.args.get("next")
        # is_safe_url should check if the url is safe for redirects.
        # See http://flask.pocoo.org/snippets/62/ for an example.
        # if not is_safe_url(next):
        #     return flask.abort(400)

        return redirect(next_url or url_for("main.acceuil"))
    else:
        return redirect(request.url)
        # return flask.render_template("inscription.jinja", signup_form=form)
