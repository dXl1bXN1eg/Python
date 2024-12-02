import nmap

dosya_yolu = 'discovery.txt'
sozluk = {}

with open(dosya_yolu, 'r') as dosya:
    for satir in dosya:
        parcalar = satir.split(' ', 2)  
        if len(parcalar) > 0:  
            anahtar = parcalar[1]
            sozluk[anahtar] = ""  


nm = nmap.PortScanner()

for i in sozluk:
    nm.scan(i, '1-1001')
    for host in nm.all_hosts():
        print(f'Host : {host} ({nm[host].hostname()})')
        print(f'State : {nm[host].state()}')
        for proto in nm[host].all_protocols():
            print(f'Protocol : {proto}')
            ports = nm[host][proto].keys()
            for port in ports:
                print(f'Port : {port}\tState : {nm[host][proto][port]["state"]}')
        
        if 'osmatch' in nm[host]:
            for os in nm[host]['osmatch']:
                version = os.get('osclass', None)  
                if version and 'HP' in version[0].get('osfamily', ''):
                    print(f"HP Bilgisayar Tespit Edildi: {host} - {version[0].get('osfamily', 'Bilinmiyor')}")
