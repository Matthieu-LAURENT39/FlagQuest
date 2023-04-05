from . import main
from flask import render_template


@main.route("/liste_cours")
def liste_cours():
    """Page répertoriant les cours disponibles"""
    return render_template("cours.jinja")


@main.route("/cours/<cours_url_name>")
def cours(cours_url_name: str):
    """Une page qui contient les cours d'une séquence"""
    # ajouter table ??????

