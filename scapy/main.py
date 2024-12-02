from scapy.all import *

"""packet = IP(dst="8.8.8.8")/ICMP()
send(packet)"""


def packet_callback(packet):
    print(packet.show())

sniff(prn=packet_callback, count=10)