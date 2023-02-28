from ipaddress import IPv4Address, IPv4Network

import pytest

from site_elysium.classes import Allocator


@pytest.fixture
def ip_network() -> IPv4Network:
    # Un réseau avec 6 hôtes: 10.0.0.1, 10.0.0.2, ..., 10.0.0.6
    ip_network = IPv4Network("10.0.0.0/29", strict=True)

    # On vérifie que le réseau comporte bien 6 hôtes
    assert len(list(ip_network.hosts())) == 6

    return ip_network


def test_ip_allocator(ip_network):
    """
    Teste que l'Allocator alloue bien les IPs
    """

    ip_allocator = Allocator(ip_network.hosts())
    # On vérifie que les allocations se font bien dans l'ordre
    assert ip_allocator.allocate() == IPv4Address("10.0.0.1")
    assert ip_allocator.allocate() == IPv4Address("10.0.0.2")
    assert ip_allocator.allocate() == IPv4Address("10.0.0.3")
    assert ip_allocator.allocate() == IPv4Address("10.0.0.4")
    assert ip_allocator.allocate() == IPv4Address("10.0.0.5")
    assert ip_allocator.allocate() == IPv4Address("10.0.0.6")

    # Il n'y a plus d'IPs a attribué, donc une erreur devrais être levé
    with pytest.raises(ValueError):
        ip_allocator.allocate()

    # On libère deux ips
    ip_allocator.free(IPv4Address("10.0.0.3"))
    ip_allocator.free(IPv4Address("10.0.0.6"))

    # Puis on teste qu'on puisse a nouveau attribuer des IPs
    assert ip_allocator.allocate() == IPv4Address("10.0.0.3")

    # Enfin, on teste que l'on ne peut pas libéré une IP déja libre
    with pytest.raises(ValueError):
        ip_allocator.free(IPv4Address("10.0.0.6"))


def test_ip_allocator_with_allocated(ip_network):
    """
    Test que l'Allocator alloue bien les IPs quand le parametre 'allocated' est utilisé
    """

    # On créé un Allocator qui a déja les ips 10.0.0.1, 10.0.0.2, 10.0.0.4 et 10.0.0.6 d'alloué
    # Les ips libres sont donc 10.0.0.3 et 10.0.0.5
    ip_allocator = Allocator(
        ip_network.hosts(),
        allocated={
            IPv4Address("10.0.0.1"),
            IPv4Address("10.0.0.2"),
            IPv4Address("10.0.0.4"),
            IPv4Address("10.0.0.6"),
        },
    )

    # L'Allocator doit évité les ips déja attribué
    assert ip_allocator.allocate() == IPv4Address("10.0.0.3")
    assert ip_allocator.allocate() == IPv4Address("10.0.0.5")

    # Il n'y a plus d'IPs a attribué, donc une erreur devrais être levé
    with pytest.raises(ValueError):
        ip_allocator.allocate()
