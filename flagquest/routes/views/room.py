"""
Endpoints lié aux rooms
"""

from . import main
from flask import render_template
from flask_login import current_user


@main.route("/liste_rooms")
def liste_room():
    """Une liste de l'intégralité des rooms"""
    from ...models import Room

    # On affiche les rooms par ordre alphabétique
    rooms = sorted(Room.query.all(), key=lambda r: r.name.casefold())
    return render_template("liste_rooms.jinja", rooms=rooms)


@main.route("/room/<room_url_name>")
def room(room_url_name: str):
    """Une room, avec affichage des questions"""
    from ...models import Room, VirtualMachine

    # cherche le nom la room entré dans l'url dans toute le bdd
    # si pas trouvé --> abandonne avec 404
    room: Room = Room.query.filter_by(url_name=room_url_name).first_or_404(
        description="Cette room n'existe pas."
    )

    # si l'user est co
    if current_user.is_authenticated:
        # calculer sa progression
        nbr_question_solved = sum(q.is_solved_by(current_user) for q in room.questions)

        # liste les vm attribué à l'user si c'est le cas
        user_existing_vms = VirtualMachine.query.filter_by(
            user_id=current_user.id
        ).all()

        user_attack_vm: VirtualMachine | None = (
            VirtualMachine.query.filter_by(user_id=current_user.id)
            .filter(VirtualMachine.display_port.isnot(None))
            .first()
        )
    else:
        nbr_question_solved = 0
        user_existing_vms = None
        user_attack_vm = None

    # from flagquest.vm import get_vm_manager

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
        user_attack_vm=user_attack_vm,
    )
    # try:
    #     return render_template(f"room/{room.url_name}.jinja", room=room)
    # except TemplateNotFound:
    #     abort(404)


@main.route("/room/supervision/<room_url_name>")
def supervision(room_url_name: str):
    """Supervision du site."""
    from ...models import Room

    room: Room = Room.query.filter_by(url_name=room_url_name).first_or_404(
        description="Cette room n'existe pas."
    )

    user_dico = {}
    for u in room.users:
        user_score = sum(q.is_solved_by(u) for q in room.questions)
        user_dico[u] = user_score

    user_dico = dict(sorted(user_dico.items(), key=lambda x: x[1], reverse=True))

    return render_template(
        "supervision.jinja",
        room=room,
        user_dico=user_dico,
    )
