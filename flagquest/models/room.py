"""
Modèle SQLAlchemy représentant une room
"""
from __future__ import annotations

from . import _current_base, _current_relationship
from sqlalchemy.orm import Mapped, mapped_column
from . import room_user
from typing import Optional, TYPE_CHECKING


if TYPE_CHECKING:
    from . import User, Question


class Room(_current_base):
    """Une room regroupant des questions et des consignes"""

    __tablename__ = "rooms"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str]
    """Le nom qui est affiché à l'utilisateur"""
    url_name: Mapped[str] = mapped_column(unique=True)
    """Le nom utilisé dans les URLs"""

    description: Mapped[str]
    """Une courte description de la room. Utilisé en dehors de la room afin d'expliquer son sujet. Peut contenir du markdown."""

    instructions: Mapped[str]
    """Les consignes de la room, affiché au dessus des questions. Peut contenir du markdown."""

    users: Mapped[list["User"]] = _current_relationship(
        secondary=room_user, back_populates="joined_rooms"
    )

    questions: Mapped[list["Question"]] = _current_relationship(
        back_populates="room", cascade="all, delete, delete-orphan"
    )

    _victim_vm_ids: Mapped[str] = mapped_column("victim_vm_ids", default="")
    """Les IDs des templates des machines victimes de la room, séparé par des points virgule ';'."""

    @property
    def victim_vm_ids(self) -> list[int]:
        """Les IDs des templates des machines victimes de la room"""
        if not self._victim_vm_ids:
            return []
        return [int(v) for v in self._victim_vm_ids.split(";")]

    @victim_vm_ids.setter
    def victim_vm_ids(self, value: list[int]):
        self._victim_vm_ids = ";".join(str(v) for v in value)
