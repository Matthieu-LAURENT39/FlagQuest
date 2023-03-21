from . import main
from flask import render_template


@main.route("/profile")
def profile():
    return render_template("profile.jinja")


@main.route("/classement")
def classement():
    from ...models import User

    # tri par ordre score : décroissant
    user = User.query.order_by(User.score.desc()).all()

    # compte nombre total d'utilisateurs
    nbr_user = User.query.count()
    return render_template("classement.jinja", user=user, nbr_user=nbr_user)
