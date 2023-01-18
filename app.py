from flask import Flask, render_template


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

    signup_form = SignupForm()
    return render_template("acceuil.jinja", signup_form=signup_form)


@app.route("/header")
def header():
    return render_template("header.jinja")


# test header une fois connecté
@app.route("/header2")
def header2():
    return render_template("header2test.jinja")


# test tout court
@app.route("/test")
def test():
    return render_template("test.jinja")


@app.route("/room/<nom_room>")
def room(nom_room: str):
    return render_template(f"room/{nom_room}.jinja")
