import nmap

nm = nmap.PortScanner()

nm.scan('127.0.0.1', '1-65535')
for host in nm.all_hosts():
    print(f'Host : {host} ({nm[host].hostname()})')
    print(f'State : {nm[host].state()}')
    for proto in nm[host].all_protocols():
        print(f'Protocol : {proto}')
        ports = nm[host][proto].keys()
        for port in ports:
            print(f'Port : {port}\tState : {nm[host][proto][port]["state"]}')
