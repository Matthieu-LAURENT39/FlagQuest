import json
from ipaddress import IPv4Address, IPv4Network

MAC_ADDRESS_LENGHT = 6
IP_BYTES_LENGHT = 4


def ip_to_mac(ip: IPv4Address) -> str:
    padded_ip = ip.packed.rjust(MAC_ADDRESS_LENGHT, b"\0")

    return ":".join(f"{d:02x}" for d in padded_ip)


def mac_to_ip(mac: str) -> IPv4Address:
    mac_bytes_str = mac.split(":")[-IP_BYTES_LENGHT:]
    ip_dec_str = [str(int(b, 16)) for b in mac_bytes_str]
    return IPv4Address(".".join(ip_dec_str))


# print(ip_to_mac(IPv4Address("192.168.1.1")))
# print(mac_to_ip("00:00:c0:a8:01:01"))

test_ip = IPv4Address("192.168.1.1")
# On test que la conversion marche dans les deux sens sans perte de données.
assert mac_to_ip(ip_to_mac(test_ip)) == test_ip

if __name__ == "__main__":
    network_str = input("Enter the network ip (XX.XX.XX.XX/XX)\n> ")
    network = IPv4Network(network_str, strict=True)

    ip_to_mac_dict = {h.compressed: ip_to_mac(h) for h in network.hosts()}

    mac_to_ip_dict = {mac: ip for ip, mac in ip_to_mac_dict.items()}

    with open("ip_to_mac.json", "w") as f:
        json.dump(ip_to_mac_dict, f, indent=0)

    with open("mac_to_ip.json", "w") as f:
        json.dump(mac_to_ip_dict, f, indent=0)

    with open("ethers", "w") as f:
        f.write("# /etc/ethers\n")
        f.write(
            "# Automatic mapping, encoding the IP in the last bytes of the mac address\n"
        )
        for ip, mac in ip_to_mac_dict.items():
            f.write(f"{mac}\t{ip}\n")
