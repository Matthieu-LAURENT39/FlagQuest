import ipaddress

from proxmoxer import ProxmoxAPI

from site_elysium.classes import Allocator, ProxmoxVMManager
import site_elysium.models
from tools import ip_to_mac
from flask import current_app

_current_vm_manager = None


def get_vm_manager() -> ProxmoxVMManager:
    global _current_vm_manager
    if _current_vm_manager is None:
        _proxmox_api = ProxmoxAPI(
            current_app.config["PROXMOX_IP"],
            user=current_app.config["PROXMOX_LOGIN"],
            password=current_app.config["PROXMOX_PASSWORD"],
            verify_ssl=current_app.config["PROXMOX_VERIFY_SSL"],
        )

        with current_app.app_context():
            _allocated_macs: set[str] = {
                vm.mac_address for vm in site_elysium.models.VirtualMachine.query.all()
            }
            _allocated_ports: set[int] = {
                vm.display_port for vm in site_elysium.models.VirtualMachine.query.all()
            }

        _mac_allocator = Allocator(
            (
                ip_to_mac(ip)
                for ip in ipaddress.IPv4Network(
                    current_app.config["VM_NETWORK"]
                ).hosts()
            ),
            allocated=_allocated_macs,
        )

        _display_port_allocator = Allocator(
            iter(range(1, 5000)), allocated=_allocated_ports
        )

        _current_vm_manager = ProxmoxVMManager(
            _proxmox_api,
            "rootme",
            _mac_allocator,
            _display_port_allocator,
        )

    return _current_vm_manager
