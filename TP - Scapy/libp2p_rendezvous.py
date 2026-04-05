#!/usr/bin/env python

import enum
import random
from scapy.all import *
from scapy.layers.inet import IP, UDP
from scapy.packet import Packet, bind_layers
from scapy.fields import ByteField, StrField, IntField, FieldLenField


class MessageType(enum.Enum):
    REGISTER = 0
    REGISTER_RESPONSE = 1
    UNREGISTER = 2
    DISCOVER = 3
    DISCOVER_RESPONSE = 4


class RendezvousMessage(Packet):
    fields_desc = [
        ByteEnumField("type", enum=MessageType, default=0),
        FieldLenField("ns_len", fmt="B", length_of="namespace", default=None),
        StrLenField("namespace", length_from=lambda p: p.ns_len, default=b''),
        IntField("ttl", default=2*3600),  # 2h en secondes
        FieldLenField("peerid_len", fmt="B", length_of="peerid", default=None),
        StrLenField("peerid", length_from=lambda p: p.peerid_len, default=b''),
    ]

bind_layers(UDP, RendezvousMessage, dport=1234)


print("Sérialisation et désérialisation")
print("================================")

# Création de message.
p = RendezvousMessage(type=1, namespace="test", peerid="QmPeerID")
print("Message créé :")
p.show()

# Sérialisation.
b: bytes = p.build()
print(f"Buffer sérialisé : {b.hex()!r}")
print("")

# Désérialisation.
p = RendezvousMessage(b)
print("Message désérialisé :")
p.show()


print("Empilements protocolaires")
print("=========================")

# Création de message.
p = (
    Ether()
    / IP(dst="127.0.0.1")
    / UDP(sport=random.randint(1025, 0xffff))  # Port source aléatoire.
    / RendezvousMessage(type=1, namespace="test", ttl=3600, peerid="QmPeerID")
)
print("Message Ethernet créé :")
p.show()
print("Message UDP :")
p[UDP].show()

# Sérialisation.
b: bytes = p.build()
print(f"Buffer Ethernet sérialisé : {b.hex()!r}")

# Désérialisation.
p = Ether(b)
print(f"Message Ethernet désérialisé :")
p.show()
