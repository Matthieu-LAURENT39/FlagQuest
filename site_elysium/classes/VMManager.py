from __future__ import annotations

import time
from threading import Lock
from typing import Optional

from proxmoxer import ProxmoxAPI

from ..classes import Allocator


class VMManager:
    """
    Gere les interactions avec l'hyperviseur (proxmox) ainsi que la gestion des VMs
    """

    def _test_auth(self) -> bool:
        """Renvois True si notre api token est valide, sinon raise un erreur"""
        # Va faire un erreur 401 si l'auth n'est pas valide
        self.api.get()
        return True

    def __init__(
        self,
        api: ProxmoxAPI,
        node_name: str,
        mac_manager: Allocator[str],
        display_port_manager: Allocator[int],
    ) -> None:
        """Initialise la classe

        Args:
            api: (ProxmoxAPI): le client proxmox à utiliser
            node_name (str): Le nom du node promox sur lequel stocker les VMs.
            mac_manager (Allocator[str]): Un Allocator gérant l'allocation des adresses MAC.
            display_port_manager (Allocator[int]): Un Allocator gérant l'allocation des display ports.

        Raises:
            ValueError: api_token n'étais pas valide
        """
        self.api = api
        self.node_name = node_name
        self._vm_modification_lock = Lock()
        """Pour éviter les race-conditions lors des opérations sur les VMs"""

        self._mac_manager = mac_manager
        self._display_port_manager = display_port_manager

        self._test_auth()

    def _get_free_vm_id(self) -> int:
        """Obtient un id disponible pour une VM.

        Returns:
            int: Un ID disponible
        """
        return self.api.cluster.get("nextid")

    def _clone_vm(
        self, cloned_vm_id: int, name: str, *, wait_until_done: bool = True
    ) -> int:
        """Créer un clone d'une VM.

        Args:
            cloned_vm_id (int): L'id de la machine à cloner.
            wait_until_done (bool): Attent que la machine soit cloné.

        Returns:
            int: L'id de la nouvelle VM.
        """
        # On utilise un lock afin d'éviter les race conditions avec les IDs
        with self._vm_modification_lock:
            new_vm_id = self._get_free_vm_id()

            # On obtient la VM à cloner
            to_clone = self.api.nodes(self.node_name).qemu(cloned_vm_id)
            # Puis on la clone
            upid = to_clone.clone.post(newid=new_vm_id, name=name)

            if wait_until_done:
                # On attend que le clonage soit fini
                task_info: dict = (
                    self.api.nodes(self.node_name).tasks(upid).status.get()
                )
                while task_info["status"] == "running":
                    task_info = self.api.nodes(self.node_name).tasks(upid).status.get()
                    time.sleep(1)

                assert task_info["exitstatus"] == "OK"

        return new_vm_id

    # def get_vnc_url(self, vm_id: int) -> str:
    #     # First we get the ticket for auth
    #     vnc_data = self.api.nodes(self.node_name).qemu(vm_id).vncproxy.post()
    #     print(vnc_data)
    #     ticket = vnc_data["ticket"]
    #     port = vnc_data["port"]
    #     # print(urllib.parse.quote_plus(ticket))

    #     return f"https://172.17.50.250:8006/?console=shell&xtermjs=1&vmid={vm_id}&vmname=&node=cooldomain&cmd="

    #     return f"wss://172.17.50.250:8006/api2/json/nodes/cooldomain/lxc/101/vncwebsocket?port={port}&vncticket={urllib.parse.quote_plus(ticket)}"
    #     return f"https://172.17.50.250:8006/api2/json/nodes/cooldomain/lxc/101/vncwebsocket?port={port}&vncticket={urllib.parse.quote_plus(ticket)}"
    #     return f"wss://172.17.50.250:8006/api2/json/nodes/{self.node_name}/lxc/{vm_id}/vncwebsocket?port={port}&vncticket={ticket}"

    def _enable_vnc(
        self, vm_id: int, display_port: int, password: Optional[str] = None
    ):
        """Active VNC pour une VM. Si la VM est déja allumé, alors il faudra la redémaré.

        Args:
            vm_id (int): L'ID de la VM à laquelle donnée un accès VNC.
            display_port (int): Le display port. Le port qu'il faudra VNC est display_port + 5900.
            password (Optional[str], optional): Le mot de passe pour accéder au VNC. Si c'est None, aucun mot de passe ne sera demandé. Defaults to None.
        """
        if password is not None:
            raise NotImplementedError()

        args = f"-vnc 0.0.0.0:{display_port}"
        # port = 5900 + display_port
        self.api.nodes(self.node_name).qemu(vm_id).config.post(args=args)

    def _run_command(self, vm_id: int, command: str) -> str:
        """Lance une commande sur une machine virtuelle. Il faut que l'agent QEMU soit installer sur la VM.

        Args:
            vm_id (int): L'ID de la machine virtuelle.
            command (str): La commande.

        Returns:
            str: La sortie de la commande.
        """
        return (
            self.api.nodes(self.node_name).qemu(vm_id).agent.exec.post(command=command)
        )

    def _set_mac(self, vm_id: int, mac_address: str):
        """Défini l'adresse mac d'une machine virtuelle

        Args:
            vm_id (int): L'ID de la machine virtuelle à qui donnée l’adresse.
            mac_address (str): L'adresse mac, de la forme 'AA:BB:CC:DD:EE:FF'
        """
        self.api.nodes(self.node_name).qemu(vm_id).config.post(
            net0=f"virtio,macaddr={mac_address}"
        )

    def start_vm(self, vm_id: int, *, wait_until_on: bool = True):
        """Allume une machine virtuelle.

        Args:
            vm_id (int): L'id de la machine virtuelle.
            wait_until_on (bool): Bloque jusque à ce que la VM soit en ligne.
        """
        self.api.nodes(self.node_name).qemu(vm_id).status.start.post()
        if wait_until_on:
            # Tant que le status de la VM n'est pas "running"
            while (
                self.api.nodes(self.node_name)
                .qemu(vm_id)
                .status.current.get()["status"]
                != "running"
            ):
                time.sleep(1)

    def stop_vm(self, vm_id: int, *, wait_until_off: bool = True):
        """Eteind une machine virtuelle.

        Args:
            vm_id (int): L'id de la machine virtuelle.
            wait_until_off (bool): Bloque jusque à ce que la VM soit hors ligne.
        """
        self.api.nodes(self.node_name).qemu(vm_id).status.stop.post()
        if wait_until_off:
            # Tant que le status de la VM n'est pas "running"
            while (
                self.api.nodes(self.node_name)
                .qemu(vm_id)
                .status.current.get()["status"]
                != "stopped"
            ):
                time.sleep(1)

    def setup(self, template_id: int, vm_name: str, vnc: bool = False) -> dict:
        """Met en place une machine virtuelle à partir d'un template, avec une addresse IP,
        optionellement VNC. Il ne reste plus qu'a stoquer ces informations dans la base de donnée.

        Args:
            template_id (int): L'ID du template à cloné.
            vnc (bool, optional): Si True, alors un display port VNC sera alloué à la VM. Defaults to False.

        Returns:
            VirtualMachine: Les informations de la machine virtuelle.
        """

        # Première étape, cloner le template
        new_vm_id = self._clone_vm(template_id, name=vm_name, wait_until_done=True)

        # Deuxième étape, on défini l'adresse MAC de la VM
        mac_address = self._mac_manager.allocate()
        self._set_mac(new_vm_id, mac_address)

        # Troisième étape, on active VNC pour la VM
        if vnc:
            display_port = self._display_port_manager.allocate()
            self._enable_vnc(new_vm_id, display_port)
        else:
            display_port = None

        # Enfin, on démare la VM.
        self.start_vm(new_vm_id, wait_until_on=True)

        return {
            "mac_address": mac_address,
            "display_port": display_port,
            "vm_id": new_vm_id,
        }

    def delete_vm(self, vm_id: int):
        """Supprime une VM sur proxmox.

        Args:
            vm_id (int): L'ID de la VM à supprimer.
        """
        # On ne peut pas supprimer une VM qui est allumé
        self.stop_vm(vm_id)
        self.api.nodes(self.node_name).qemu(vm_id).delete()

    # def get_vnc_token(self, vm_id: int) -> str:
    #     proxy_data = (
    #         self.api.nodes(self.node_name)
    #         .qemu(vm_id)
    #         .vncproxy.post(websocket=1)  # , **{"generate-password": 1})
    #     )
    #     print(proxy_data)

    #     # websocket_data = (
    #     #     self.api.nodes(self.node_name)
    #     #     .qemu(vm_id)
    #     #     .vncwebsocket.get(
    #     #         port=proxy_data["port"],
    #     #         vncticket=proxy_data["ticket"],
    #     #     )
    #     # )

    #     ticket = self.api.get_tokens()[0]
    #     # print(websocket_data)
    #     # port =  int(websocket_data["port"])

    #     path = urllib.parse.quote(
    #         f"api2/json/nodes/{self.node_name}/qemu/{vm_id}/vncwebsocket?port={proxy_data['port']}&vncticket={urllib.parse.quote(proxy_data['ticket'], safe='')}",
    #         safe="",
    #     )
    #     # vnc_url = f"https://novnc.com/noVNC/vnc.html?host=172.17.50.250&port=8006&autoconnect=true&resize=scale&encrypt=1&path={path}"
    #     # vnc_url = f"http://172.17.50.249:5900/vnc.html?password={urllib.parse.quote(proxy_data['password'])}&autoconnect=true&resize=scale&encrypt=1"

    #     vnc_url = f"https://172.17.50.250:8006/?console=kvm&novnc=1&node={self.node_name}&resize=1&vmid={vm_id}&path=api2/json/nodes/{self.node_name}/qemu/{vm_id}/vncwebsocket/port/{proxy_data['port']}/vncticket/{urllib.parse.quote(proxy_data['ticket'], safe='')}"
    #     print(proxy_data["port"])
    #     return vnc_url
