import json
import time

import werkzeug.exceptions
from flask import Blueprint, Response, abort, current_app, jsonify, redirect, request
from flask_login import current_user, login_required
from flask_restx import Api, Namespace, Resource

from ... import db
from ... import models as models
from ...models import Room, VirtualMachine
from ...models.schemas import question_schema, room_schema, user_schema
from .. import api
from . import api_manager

# Type hinting
current_user: models.User

vm_namespace = Namespace(
    "VM", description="Opérations liés aux machines virtuelles.", path="/"
)


@vm_namespace.route("/can_create_victim_vm")
class CanCreateVictimVmResource(Resource):
    method_decorators = [login_required]

    def get(self):
        """Permet a l'utilisateur de savoir si il peut créer une VM victime"""
        user_victim_vms: list[VirtualMachine] = (
            VirtualMachine.query.filter_by(user_id=current_user.id)
            .filter(VirtualMachine.display_port.is_(None))
            .first()
        )

        return {"can_create_victim_vm": user_victim_vms is None}


@vm_namespace.route("/get_existing_attack_vm")
class GetExistingAttackVmResource(Resource):
    method_decorators = [login_required]

    def get(self):
        """Obtient des informations sur la VM d'attaque existante"""

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


@vm_namespace.route("/get_existing_victim_vm/<room_url_name>")
class GetExistingVictimVmResource(Resource):
    method_decorators = [login_required]

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

        vm_data = [
            {
                "ip_address": vm.ip_address.compressed,
            }
            for vm in user_victim_vms
        ]
        return vm_data


@vm_namespace.route("/request_attack_vm")
class RequestAttackVmResource(Resource):
    method_decorators = [login_required]

    def post(self):
        """
        Créer une VM d'attaque, ou réutilise une VM existante si l'utilisateur en a déja une.
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


@vm_namespace.route("/request_victim_vms/<room_url_name>")
class RequestVictimVmsResource(Resource):
    method_decorators = [login_required]

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
class DeleteVmsResource(Resource):
    method_decorators = [login_required]

    def post(self):
        """Supprime toutes les VMs de l'utilisateur"""
        from vm import get_vm_manager

        vm_manager = get_vm_manager()

        vms: list[models.VirtualMachine] = models.VirtualMachine.query.filter_by(
            user_id=current_user.id
        ).all()

        for vm in vms:
            vm_manager.delete_vm(vm.proxmox_id)
            db.session.delete(vm)

        db.session.commit()
        # Wait a bit to avoid race conditions
        time.sleep(0.1)
        return {}
