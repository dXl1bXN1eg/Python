from scapy.all import *

# Create and send an ICMP packet
packet = IP(dst="8.8.8.8")/ICMP()
send(packet)

# Sniff packets on the network
packets = sniff(count=10)
packets.summary()
