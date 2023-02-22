from . import main
from flask import render_template
from flask_login import current_user


@main.route("/liste_rooms")
def liste_room():
    from ...forms import SignupForm
    from ...models import Room

    signup_form = SignupForm()
    rooms = Room.query.all()
    return render_template("liste_rooms.jinja", signup_form=signup_form, rooms=rooms)


@main.route("/room/<room_url_name>")
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
        "room.jinja", room=room, nbr_question_solved=nbr_question_solved
    )
    # try:
    #     return render_template(f"room/{room.url_name}.jinja", room=room)
    # except TemplateNotFound:
    #     abort(404)


@main.route("/room/<room_url_name>/edit")
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
        "edit_room.jinja", room=room, nbr_question_solved=nbr_question_solved
    )
