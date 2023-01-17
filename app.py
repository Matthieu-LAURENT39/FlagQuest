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
    return render_template("acceuil.jinja")


@app.route("/inscription")
def inscription():
    return render_template("inscription.jinja")


@app.route("/connection")
def connexion():
    return render_template("connection.jinja")


@app.route("/vnc")
def vnc():
    return render_template("vnc.html")
