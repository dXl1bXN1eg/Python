from scapy.all import *

# Discover network devices
arp_request = ARP(pdst="192.168.1.1/24")
broadcast = Ether(dst="ff:ff:ff:ff:ff:ff")
arp_request_broadcast = broadcast/arp_request
answered_list = srp(arp_request_broadcast, timeout=1, verbose=False)[0]

for element in answered_list:
    print(f"IP: {element[1].psrc} MAC: {element[1].hwsrc}")




def scan_ports(ip, start_port, end_port):
    for port in range(start_port, end_port + 1):
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(1)
        result = sock.connect_ex((ip, port))
        if result == 0:
            print(f"Port {port} is open")
        sock.close()

scan_ports("192.168.1.1", 20, 80)