from .. import db
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy_utils import UUIDType
from flask import current_app
from uuid import uuid4, UUID
from tools import mac_to_ip
from ipaddress import IPv4Address
from typing import Optional


# class VMType(enum.Enum):
#     attack = "attack"
#     victim = "victim"


class VirtualMachine(db.Model):
    """Une room regroupant des questions et des consignes"""

    __tablename__ = "virtual_machines"

    def __init__(self, *args, **kwargs) -> None:
        self.uuid = uuid4()
        super().__init__(*args, **kwargs)

    uuid: Mapped[UUID] = mapped_column(UUIDType, primary_key=True)
    proxmox_id: Mapped[int] = mapped_column(unique=True)

    user_id: Mapped[int]
    """L'id de l'utilisateur à qui appartient là VM"""

    template_vm_id: Mapped[int]
    """L'ID de la VM template sur laquel est basé cette VM"""

    room_id: Mapped[Optional[int]]
    """L'ID de la room qui correspond a cette VM. None pour les VMs d'attaques."""

    # type: VMType = Column(Enum(VMType)) # noqa: F723
    # """Le type de machine virtuelle"""

    # ip_address = Column(IPAddressType, unique=True, nullable=False)
    # """L'addresse IP sur le réseau réservé au VMs."""

    mac_address: Mapped[str] = mapped_column(unique=True)
    """L'addresse MAC sur le réseau réservé au VMs."""

    display_port: Mapped[Optional[int]] = mapped_column(unique=True)
    """Le display port VNC de la VM. Le port VNC associé est 5900+display_port. Les machines victimes n'en ont pas"""

    @property
    def vm_name(self) -> str:
        """Le nom de la VM dans proxmox."""
        return f"{current_app.config['VICTIM_VM_PREFIX']}-{self.uuid.hex}"

    @property
    def ip_address(self) -> IPv4Address:
        """L'adresse IP de la machine virtuele, basé sur son adresse MAC"""
        return mac_to_ip(self.mac_address)

    @property
    def vnc_port(self) -> int | None:
        """Le port VNC de la machine virtuelle."""
        if self.display_port is None:
            return None
        return self.display_port + 5900
