from flask import Flask, render_template, abort
from flask_login import current_user

app = Flask(
    __name__,
    static_folder="static",
    template_folder="templates",
    static_url_path="/static",
)
app.config["SECRET_KEY"] = "ChangeMeIAmNotSecure"


@app.route("/")
def acceuil():
    from site_elysium.backend import SignupForm
    from site_elysium.models import Room

    signup_form = SignupForm()
    rooms = Room.query.limit(4).all()
    return render_template("acceuil.jinja", signup_form=signup_form, rooms=rooms)


@app.route("/liste_rooms")
def liste_room():
    from site_elysium.backend import SignupForm
    from site_elysium.models import Room

    signup_form = SignupForm()
    rooms = Room.query.all()
    return render_template("liste_rooms.jinja", signup_form=signup_form, rooms=rooms)


@app.route("/header")
def header():
    return render_template("header.jinja")


@app.route("/profile")
def profile():
    return render_template("profile.jinja")


@app.route("/classement")
def classement():
    from site_elysium.models import User

    # tri par ordre score : décroissant
    user = User.query.order_by(User.score.desc()).all()

    # compte nombre total d'utilisateurs
    nbr_user = User.query.count()
    return render_template("classement.jinja", user=user, nbr_user=nbr_user)


@app.route("/liste_rooms")
def liste_rooms():
    return render_template("liste_rooms.jinja")


@app.route("/room/<room_url_name>")
def room(room_url_name: str):
    from site_elysium.models import Room

    room: Room = Room.query.filter_by(url_name=room_url_name).first_or_404(
        description="Cette room n'existe pas."
    )

    if current_user.is_authenticated:
        nbr_question_solved = sum(q.is_solved_by(current_user) for q in room.questions)
    else:
        nbr_question_solved = None

    return render_template(
        f"room.jinja", room=room, nbr_question_solved=nbr_question_solved
    )
    # try:
    #     return render_template(f"room/{room.url_name}.jinja", room=room)
    # except TemplateNotFound:
    #     abort(404)


@app.route("/room/<room_url_name>/edit")
def edit_room(room_url_name: str):
    from site_elysium.models import Room

    room: Room = Room.query.filter_by(url_name=room_url_name).first_or_404(
        description="Cette room n'existe pas."
    )

    if current_user.is_authenticated:
        nbr_question_solved = sum(q.is_solved_by(current_user) for q in room.questions)
    else:
        nbr_question_solved = None

    return render_template(
        f"edit_room.jinja", room=room, nbr_question_solved=nbr_question_solved
    )


# dashboard administrateur
@app.route("/dashboard")
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
