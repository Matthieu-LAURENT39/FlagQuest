from . import main
from flask import render_template, make_response
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
    from site_elysium.models import Room, VirtualMachine

    room: Room = Room.query.filter_by(url_name=room_url_name).first_or_404(
        description="Cette room n'existe pas."
    )

    if current_user.is_authenticated:
        nbr_question_solved = sum(q.is_solved_by(current_user) for q in room.questions)
        user_existing_vms = VirtualMachine.query.filter_by(
            user_id=current_user.id
        ).all()
    else:
        nbr_question_solved = None
        user_existing_vms = None

    # from vm import get_vm_manager

    # vm_manager = get_vm_manager()
    # # vnc_url = f"https://172.17.50.250:8006/vnc.html?host=172.17.50.250&port=6080&autoconnect=true&resize=scale"
    # # vnc_url = "https://172.17.50.250:8006/?console=kvm&novnc=1&vmid=103&vmname=test&node=rootme&resize=off&cmd="

    # try:
    #     vnc_url = vm_manager.get_vnc_token(103)
    # except Exception:
    #     vnc_url = ""

    return render_template(
        "room.jinja",
        room=room,
        nbr_question_solved=nbr_question_solved,
        user_existing_vms=user_existing_vms,
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
