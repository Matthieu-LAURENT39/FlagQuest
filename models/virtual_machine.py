from backend.db import db
from sqlalchemy import Integer, Column, String, Enum
import enum
from sqlalchemy_utils import IPAddressType, UUIDType
from uuid import uuid4
from tools import mac_to_ip
from ipaddress import IPv4Address


# class VMType(enum.Enum):
#     attack = "attack"
#     victim = "victim"


class VirtualMachine(db.Model):
    """Une room regroupant des questions et des consignes"""

    __tablename__ = "virtual_machines"

    id = Column(UUIDType, primary_key=True, default=uuid4)

    user_id = Column(Integer)
    """L'id de l'utilisateur à qui appartient là VM"""

    template_vm_id = Column(Integer)
    """L'ID de la VM template sur laquel est basé cette VM"""

    # type: VMType = Column(Enum(VMType))
    # """Le type de machine virtuelle"""

    # ip_address = Column(IPAddressType, unique=True, nullable=False)
    # """L'addresse IP sur le réseau réservé au VMs."""

    mac_address = Column(String, unique=True, nullable=False)
    """L'addresse MAC sur le réseau réservé au VMs."""

    display_port = Column(Integer, unique=True, nullable=True)
    """Le display port VNC de la VM. Le port VNC associé est 5900+display_port. Les machines victimes n'en ont pas"""

    @property
    def vm_name(self) -> str:
        """Le nom de la VM dans proxmox."""
        return f"automatic-{self.user_id}-{self.template_vm_id}"

    @property
    def ip_address(self) -> IPv4Address:
        """L'adresse IP de la machine virtuele, basé sur son adresse MAC"""
        return mac_to_ip(self.mac_address)