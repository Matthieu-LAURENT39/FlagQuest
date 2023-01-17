from flask import Flask, render_template

app = Flask(
    __name__,
    static_folder="static",
    template_folder="templates",
    static_url_path="/static",
)


@app.route("/")
def acceuil():
    return render_template("acceuil.jinja")


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


@app.route("/inscription")
def inscription():
    return render_template("inscription.jinja")


@app.route("/connection")
def connection():
    return render_template("connection.jinja")


@app.route("/room/<nom_room>")
def room(nom_room: str):
    return render_template(f"room/{nom_room}.jinja")

app.run("0.0.0.0", 8080, debug=True)
