from classes.VirtualMachine import VirtualMachine
from threading import Lock
from proxmoxer import ProxmoxAPI
from uuid import uuid4
import time
from typing import Optional


class ProxomoxManager:
    """
    Gere les interactions avec l'hyperviseur proxmox
    """

    def _test_auth(self) -> bool:
        """Renvois True si notre api token est valide, sinon raise un erreur"""
        # Va faire un erreur 401 si l'auth n'est pas valide
        self.api.get()
        return True

    def __init__(self, api: ProxmoxAPI, node_name: str) -> None:
        """Initialise la classe

        Args:
            api: (ProxmoxAPI): le client proxmox à utiliser
            node_name (str): Le nom du node promox sur lequel stocker les VMs.

        Raises:
            ValueError: api_token n'étais pas valide
        """
        self.api = api
        self.node_name = node_name
        self._vm_modification_lock = Lock()
        """Pour éviter les race-conditions lors des opérations sur les VMs"""
        self._test_auth()

    def _get_free_vm_id(self) -> int:
        """Obtient un id disponible pour une VM.

        Returns:
            int: Un ID disponible
        """
        return self.api.cluster.get("nextid")

    def clone_vm(self, cloned_vm_id: int, wait_until_done: bool = True) -> int:
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
            upid = to_clone.clone.post(newid=new_vm_id, name=str(uuid4()))

            if wait_until_done:
                # On attend que le clonage soit fini
                task_info = self.api.nodes(self.node_name).tasks(upid).status.get()
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

    def _set_vnc_password(self, vm_id: int, password: str):
        raise NotImplementedError()
        # self.api.

    def enable_vnc(self, vm_id: int, port: int, password: Optional[str] = None):
        """Active VNC pour une VM. Si la VM est déja allumé, alors il faudra la redémaré.

        Args:
            vm_id (int): L'ID de la VM à laquelle donnée un accès VNC.
            port (int): Le port qui sera utilisé pour accedé à cette VM en VNC.
            password (Optional[str], optional): Le mot de passe pour accéder au VNC. Si c'est None, aucun mot de passe ne sera demandé. Defaults to None.
        """
        args = f"-vnc 0.0.0.0:{port}"
        if password is not None:
            # Enable password
            args += ",password=on"
            # Then set it
            self._set_vnc_password(vm_id, password)

        self.api.nodes(self.node_name).qemu(vm_id).config.post(args=args)

    def start_vm(self, vm_id: int, wait_until_on: bool = True):
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
