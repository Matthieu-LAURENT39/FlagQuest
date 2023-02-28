from flask import render_template
from flask_login import current_user

from . import main


# dashboard administrateur
@main.route("/dashboard")
def dashboard():
    from site_elysium.models import User

    # liste tout les utilisateurs
    user = User.query.all()

    # compte nombre total d'user - 1 (compte admin ?)
    nbr_user = User.query.count()

    # si user est co & si user est admin
    if current_user.is_authenticated and current_user.is_admin == True:
        # autoriser a accéder au site
        return render_template("admin_dashboard.jinja", user=user, nbr_user=nbr_user)
    else:
        # page erreur
        return render_template("/errors/404.jinja")
