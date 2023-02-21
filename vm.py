import ipaddress

from proxmoxer import ProxmoxAPI

from site_elysium.app import app
from site_elysium.classes import Allocator, VMManager
import site_elysium.models
from tools import ip_to_mac

_proxmox_api = ProxmoxAPI(
    "172.17.50.250:8006",
    user="root@pam",
    password="passw0rd",
    verify_ssl=False,
)

with app.app_context():
    _allocated_macs: set[str] = {
        vm.mac_address for vm in site_elysium.models.VirtualMachine.query.all()
    }
    _allocated_ports: set[int] = {
        vm.display_port for vm in site_elysium.models.VirtualMachine.query.all()
    }

_mac_allocator = Allocator(
    (ip_to_mac(ip) for ip in ipaddress.IPv4Network("192.168.1.0/24").hosts()),
    allocated=_allocated_macs,
)

_display_port_allocator = Allocator(iter(range(1, 5000)), allocated=_allocated_ports)

vm_manager = VMManager(
    _proxmox_api,
    "rootme",
    _mac_allocator,
    _display_port_allocator,
)
