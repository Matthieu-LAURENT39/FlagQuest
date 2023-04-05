import json

import werkzeug.exceptions
from flask import Blueprint, Response, abort, jsonify, redirect, request, current_app
from flask_login import current_user, login_required
from flask_restful import Api, Resource

from ... import models as models
from ...models import VirtualMachine, Room
from ...models.schemas import room_schema, user_schema

from ... import db
from .. import api

# Type hinting
current_user: models.User


class UserResource(Resource):
    """Informations lié à un utilisateur"""

    def get(self, username):
        """Récupère les informations lié a un utilisateur."""
        user: models.User = models.User.query.filter_by(username=username).first_or_404(
            description="Cet utilisateur n'existe pas."
        )
        return user_schema.dump(user)


@api.after_request
def api_after_request(r: Response) -> Response:
    """Edite toute les réponse de l'API"""
    j: dict = r.get_json()

    # Des fois il n'y a pas de data
    if isinstance(j, dict):
        # On ajoute le champ avec le succès de la requête
        j["success"] = r.status_code == 200

    r.data = json.dumps(j, indent=4)
    return r


# Formate toutes les erreurs en json
@api.errorhandler(werkzeug.exceptions.HTTPException)
def api_error_handler(error: werkzeug.exceptions.HTTPException):
    """Formatte toutes les erreurs d'API en json"""
    return {"message": error.description}, error.code


@api.route("/join_room/<room_url_name>", methods=["POST"])
@login_required
def join_room(room_url_name: str):
    """Permet a un utilisateur de rejoindre une room."""
    room: models.Room = models.Room.query.filter_by(
        url_name=room_url_name
    ).first_or_404(description="Cette room n'existe pas.")
    if current_user in room.users:
        abort(400, "L'utilisateur est deja dans la room.")
    room.users.append(current_user)
    db.session.commit()
    return {}


@api.route("/answer_question", methods=["POST"])
@login_required
def answer_question():
    """
    Permet a l'utilisateur de répondre a une question et
    de savoir si il a juste.
    """
    question_id = request.args.get("question_id")
    if question_id is None:
        abort(400, "Il manque l'argument 'question_id'")

    answer = request.args.get("answer")
    if answer is None:
        abort(400, "Il manque l'argument 'answer'")

    question: models.Question = models.Question.query.filter_by(
        id=question_id
    ).first_or_404(description="Cette question n'existe pas.")
    if current_user not in question.room.users:
        abort(400, "L'utilisateur n'est pas dans la room.")

    # TODO: vérifier si l'utilisateur à déja répondu à la question
    if question.is_solved_by(current_user):
        abort(400, "L'utilisateur a déja répondu à la question.")

    answer = request.args.get("answer")
    if answer is None:
        abort(400, "Il manque l'argument 'answer'")

    if answer.casefold().strip() != question.answer.casefold().strip():
        return {"correct": False}

    # TODO: stoqué que l'utilisateur a solve la question
    question.solve(current_user)

    return {"correct": True}


@api.route("/request_victim_vms/<room_url_name>", methods=["POST"])
@login_required
def request_victim_vms(room_url_name: str):
    """Créer les VMs victimes pour une room."""
    from vm import get_vm_manager

    # TODO: vérifier que l'utilisateur n'utilise pas déja une VM
    # We find the room
    room: models.Room = models.Room.query.filter_by(
        url_name=room_url_name
    ).first_or_404(description="Cette room n'existe pas.")

    vms_data: list[dict[str, str]] = []
    # return jsonify(
    #     [
    #         {"ip_address": "192.168.1.1", "template_vm_id": "100"},
    #         {"ip_address": "192.168.1.2", "template_vm_id": "101"},
    #     ]
    # )
    vm_manager = get_vm_manager()
    for vm_id in room.victim_vm_ids:
        new_vm_db = VirtualMachine(
            user_id=current_user.id, template_vm_id=vm_id, room_id=room.id
        )

        vm_infos = vm_manager.setup(vm_id, new_vm_db.vm_name, vnc=False)

        new_vm_db.mac_address = vm_infos["mac_address"]
        new_vm_db.display_port = vm_infos["display_port"]
        new_vm_db.proxmox_id = vm_infos["vm_id"]

        vms_data.append(
            {"ip_address": new_vm_db.ip_address.compressed, "template_vm_id": vm_id}
        )

        db.session.add(new_vm_db)

    db.session.commit()

    return jsonify(vms_data)
    # return {"ip_address": new_vm_db.ip_address.compressed}


@api.route("/get_existing_attack_vm", methods=["GET"])
@login_required
def get_existing_attack_vm():
    user_attack_vm: VirtualMachine | None = (
        VirtualMachine.query.filter_by(user_id=current_user.id)
        .filter(VirtualMachine.display_port.isnot(None))
        .first()
    )
    if user_attack_vm is None:
        return {"exists": False}

    vm_data = {
        "exists": True,
        "ip_address": current_app.config["PROXMOX_HOST"],
        "vnc_port": user_attack_vm.vnc_port,
        "username": current_app.config["ATTACK_VM_USERNAME"],
        "password": current_app.config["ATTACK_VM_PASSWORD"],
    }
    return vm_data


@api.route("/get_existing_victim_vm/<room_url_name>", methods=["GET"])
@login_required
def get_existing_victim_vm(room_url_name):
    room: Room = Room.query.filter_by(url_name=room_url_name).first_or_404(
        description="Cette room n'existe pas."
    )

    user_victim_vms: list[VirtualMachine] = (
        VirtualMachine.query.filter_by(user_id=current_user.id, room_id=room.id)
        .filter(VirtualMachine.display_port.is_(None))
        .all()
    )

    vm_data = [
        {
            "ip_address": vm.ip_address.compressed,
        }
        for vm in user_victim_vms
    ]
    return vm_data


@api.route("/can_create_victim_vm", methods=["GET"])
@login_required
def can_create_victim_vm():
    """Permet a l'utilisateur de savoir si il peut créer une VM victime"""
    user_victim_vms: list[VirtualMachine] = (
        VirtualMachine.query.filter_by(user_id=current_user.id)
        .filter(VirtualMachine.display_port.is_(None))
        .first()
    )

    return {"can_create_victim_vm": user_victim_vms is None}


@api.route("/request_attack_vm", methods=["POST"])
@login_required
def request_attack_vm():
    """
    Créer une VM d'attaque, ou réutilisé une VM existante si l'utilisateur
    en a déja une.
    """
    from vm import get_vm_manager

    user_attack_vm: VirtualMachine | None = (
        VirtualMachine.query.filter_by(user_id=current_user.id)
        .filter(VirtualMachine.display_port.isnot(None))
        .first()
    )

    if user_attack_vm is None:
        vm_manager = get_vm_manager()
        attack_vm_id = current_app.config["ATTACK_VM_TEMPLATE_ID"]
        user_attack_vm = VirtualMachine(
            user_id=current_user.id, template_vm_id=attack_vm_id
        )

        vm_infos = vm_manager.setup(attack_vm_id, user_attack_vm.vm_name, vnc=True)

        user_attack_vm.mac_address = vm_infos["mac_address"]
        user_attack_vm.display_port = vm_infos["display_port"]
        user_attack_vm.proxmox_id = vm_infos["vm_id"]

        db.session.add(user_attack_vm)

    # TODO: Utiliser un schéma marshmallow
    vm_data = {
        "ip_address": current_app.config["PROXMOX_HOST"],
        "vnc_port": user_attack_vm.vnc_port,
        "username": current_app.config["ATTACK_VM_USERNAME"],
        "password": current_app.config["ATTACK_VM_PASSWORD"],
    }

    db.session.commit()

    return jsonify(vm_data)
    # return {"ip_address": new_vm_db.ip_address.compressed}


@api.route("/delete_vms/", methods=["POST"])
@login_required
def delete_vms():
    """Supprime toute les VMs possédé par l'utilisateur."""
    from vm import get_vm_manager

    vm_manager = get_vm_manager()

    vms: list[models.VirtualMachine] = models.VirtualMachine.query.filter_by(
        user_id=current_user.id
    ).all()

    for vm in vms:
        vm_manager.delete_vm(vm.proxmox_id)
        db.session.delete(vm)

    db.session.commit()
    return {}
