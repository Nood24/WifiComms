import socket

CLIENT_IP = "192.168.1.42"
CLIENT_PORT = 65432
HOST_PORT = 65433

sockC = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

sockH = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sockH.bind(("",HOST_PORT))

sockC.sendto(b'req', (CLIENT_IP,CLIENT_PORT))

while True:
    data, addr = sockH.recvfrom(1024)
    print(float(data.decode()))

