from flask import Flask, render_template, abort
from jinja2 import TemplateNotFound

app = Flask(
    __name__,
    static_folder="static",
    template_folder="templates",
    static_url_path="/static",
)
app.config["SECRET_KEY"] = "ChangeMeIAmNotSecure"


@app.route("/")
def acceuil():
    from backend import SignupForm
    from models import Room

    signup_form = SignupForm()
    rooms = Room.query.limit(6).all()
    return render_template("acceuil.jinja", signup_form=signup_form, rooms=rooms)


@app.route("/header")
def header():
    return render_template("header.jinja")


# test header une fois connecté
@app.route("/header2")
def header2():
    return render_template("header2test.jinja")


@app.route("/profile")
def profile():
    return render_template("profile.jinja")


@app.route("/classement")
def classement():
    return render_template("classement.jinja")


# test tout court
@app.route("/test")
def test():
    return render_template("test.jinja")


@app.route("/room/<room_url_name>")
def room(room_url_name: str):
    from models import Room

    room: Room = Room.query.filter_by(url_name=room_url_name).first_or_404(
        description="Cette room n'existe pas."
    )
    return render_template(f"room.jinja", room=room)
    # try:
    #     return render_template(f"room/{room.url_name}.jinja", room=room)
    # except TemplateNotFound:
    #     abort(404)
