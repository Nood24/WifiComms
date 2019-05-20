import socket
import iperf3

CLIENT_IP = '192.168.1.43'
CLIENT_PORT = 65432
HOST_PORT = 65433
sockH = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sockH.bind(("",HOST_PORT))
sockC = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

sockC.sendto(b'req', (CLIENT_IP,CLIENT_PORT))
while True:
    data,addr = sockH.recvfrom(1024)
    dl_str = data.decode()
    DL = float(dl_str)/1000
    print(DL)
    if (dl_str == ''):
        continue
    else:
        break

client = iperf3.Client()
client.duration = 1
client.server_hostname = '192.168.1.43'
client.port = 5201
client.protocol = 'udp'
result = client.run()

if result.error:
    print(result.error)
else:
    bandwidth = result.Mbps
    total = bandwidth+DL
    print(result.Mbps)
    print('')
    print(total)

