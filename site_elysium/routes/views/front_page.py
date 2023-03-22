from . import main
from flask import render_template


@main.route("/")
def acceuil():
    """La page principale du site. Permet aussi de s'inscrire."""
    from ...forms import SignupForm
    from ...models import Room

    signup_form = SignupForm()
    rooms = Room.query.limit(4).all()
    return render_template("acceuil.jinja", signup_form=signup_form, rooms=rooms)


@main.route("/confidentalite")
def confidentalite():
    """La page de politique de confidentialité, obligatoire avec la RGPD."""
    return render_template("confidentalite.jinja")


@main.route("/mention_legales")
def mention_legales():
    """Les mentions légales du site web."""
    return render_template("mention_legales.jinja")


@main.route("/conditions_generales_d_utilisation")
def conditions_generales_d_utilisation():
    "Les conditions générales d'utilisation du site web."
    return render_template("Conditions_generales_d_utilisation.jinja")
