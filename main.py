from flask import Flask, render_template
import mimetypes

mimetypes.add_type("application/javascript", ".js")


app = Flask(
    __name__,
    static_folder="static",
    template_folder="templates",
    static_url_path="/static",
)


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


app.run("0.0.0.0", 8080, debug=True)
