from . import main
from flask import render_template


@main.route("/")
def acceuil():
    from site_elysium.forms import SignupForm
    from site_elysium.models import Room

    signup_form = SignupForm()
    rooms = Room.query.limit(4).all()
    return render_template("acceuil.jinja", signup_form=signup_form, rooms=rooms)


@main.route("/confidentalite")
def confidentalite():
    return render_template("confidentalite.jinja")


@main.route("/mention_legales")
def mention_legales():
    return render_template("mention_legales.jinja")

@main.route("/Conditions_generales_d_utilisation")
def Conditions_generales_d_utilisation():
    return render_template("Conditions_generales_d_utilisation.jinja")