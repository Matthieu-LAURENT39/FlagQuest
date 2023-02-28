from flask import render_template

from . import main


@main.route("/")
def acceuil():
    from site_elysium.forms import SignupForm
    from site_elysium.models import Room

    signup_form = SignupForm()
    rooms = Room.query.limit(4).all()
    return render_template("acceuil.jinja", signup_form=signup_form, rooms=rooms)
