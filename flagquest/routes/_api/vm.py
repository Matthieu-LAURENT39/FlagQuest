"""
Endpoints API lié aux machines virtuelles
"""

import time

from flask import current_app, jsonify
from flask_login import current_user, login_required
from flask_restx import Namespace, Resource, fields

from ... import db
from ... import models as models
from ...models import Room, VirtualMachine

# Type hinting
current_user: models.User

vm_namespace = Namespace(
    "VM", description="Opérations liés aux machines virtuelles.", path="/"
)

attack_vm_model = vm_namespace.model(
    "AttackVM",
    {
        "ip_address": fields.String,
        "password": fields.String,
        "username": fields.String,
        "vnc_port": fields.Integer,
    },
)

victim_vm_model = vm_namespace.model("VictimVM", {"ip_address": fields.String})


@vm_namespace.route("/can_create_victim_vm")
@vm_namespace.response(200, "Succès")
@vm_namespace.doc(security="http")
class CanCreateVictimVmResource(Resource):
    """Permet a l'utilisateur de savoir si il peut créer une VM victime"""

    method_decorators = [login_required]

    @vm_namespace.marshal_with(
        vm_namespace.model(
            "CanCreateVictimVM", {"can_create_victim_vm": fields.Boolean}
        )
    )
    def get(self):
        """Permet a l'utilisateur de savoir si il peut créer une VM victime"""
        user_victim_vms: list[VirtualMachine] = (
            VirtualMachine.query.filter_by(user_id=current_user.id)
            .filter(VirtualMachine.display_port.is_(None))
            .first()
        )

        return {"can_create_victim_vm": user_victim_vms is None}


@vm_namespace.route("/get_existing_attack_vm")
@vm_namespace.response(200, "Succès")
@vm_namespace.doc(security="http")
class GetExistingAttackVmResource(Resource):
    """Obtient des informations sur la VM d'attaque existante"""

    method_decorators = [login_required]

    # @vm_namespace.marshal_with(attack_vm_model, as_list=False)
    def get(self):
        """Obtient des informations sur la VM d'attaque existante"""

        user_attack_vm: VirtualMachine | None = (
            VirtualMachine.query.filter_by(user_id=current_user.id)
            .filter(VirtualMachine.display_port.isnot(None))
            .first()
        )
        if user_attack_vm is None:
            return {"exists": False}

        return {
            "exists": True,
            "ip_address": current_app.config["PROXMOX_HOST"],
            "vnc_port": user_attack_vm.vnc_port,
            "username": current_app.config["ATTACK_VM_USERNAME"],
            "password": current_app.config["ATTACK_VM_PASSWORD"],
        }


@vm_namespace.route("/get_existing_victim_vm/<room_url_name>")
@vm_namespace.response(200, "Succès")
@vm_namespace.response(404, "La room n'existe pas")
@vm_namespace.doc(security="http")
class GetExistingVictimVmResource(Resource):
    """Obtient des informations sur les VM victime existante"""

    method_decorators = [login_required]

    @vm_namespace.marshal_with(victim_vm_model, as_list=True)
    def get(self, room_url_name: str):
        """Obtient des informations sur les VM victime existante"""
        room: Room = Room.query.filter_by(url_name=room_url_name).first_or_404(
            description="Cette room n'existe pas."
        )

        user_victim_vms: list[VirtualMachine] = (
            VirtualMachine.query.filter_by(user_id=current_user.id, room_id=room.id)
            .filter(VirtualMachine.display_port.is_(None))
            .all()
        )

        return [
            {
                "ip_address": vm.ip_address.compressed,
            }
            for vm in user_victim_vms
        ]


@vm_namespace.route("/request_attack_vm")
@vm_namespace.response(200, "Succès")
@vm_namespace.doc(security="http")
class RequestAttackVmResource(Resource):
    """Créer une VM d'attaque, ou réutilise une VM existante si l'utilisateur en a déja une."""

    method_decorators = [login_required]

    @vm_namespace.marshal_with(attack_vm_model, as_list=False)
    def post(self):
        """Créer une VM d'attaque, ou réutilise une VM existante si l'utilisateur en a déja une."""
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

        vm_data = {
            "ip_address": current_app.config["PROXMOX_HOST"],
            "vnc_port": user_attack_vm.vnc_port,
            "username": current_app.config["ATTACK_VM_USERNAME"],
            "password": current_app.config["ATTACK_VM_PASSWORD"],
        }
        db.session.commit()

        return vm_data
        # return {"ip_address": new_vm_db.ip_address.compressed}


@vm_namespace.route("/request_victim_vms/<room_url_name>")
@vm_namespace.response(200, "Succès")
@vm_namespace.response(404, "La room n'existe pas")
@vm_namespace.doc(security="http")
class RequestVictimVmsResource(Resource):
    """Créer les VMs victimes pour une room."""

    method_decorators = [login_required]

    # @vm_namespace.marshal_with(victim_vm_model, as_list=True)
    def post(self, room_url_name: str):
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


@vm_namespace.route("/delete_vms/")
@vm_namespace.response(200, "Succès")
@vm_namespace.doc(security="http")
class DeleteVmsResource(Resource):
    """Permet de supprimer des VMs."""

    method_decorators = [login_required]

    def post(self):
        """Supprime toutes les VMs de l'utilisateur"""
        from vm import get_vm_manager

        vm_manager = get_vm_manager()

        vms: list[models.VirtualMachine] = models.VirtualMachine.query.filter_by(
            user_id=current_user.id
        ).all()

        for vm in vms:
            db.session.delete(vm)

        db.session.commit()
        return {}
