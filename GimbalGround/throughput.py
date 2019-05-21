import time
import psutil
import socket
import sys
import signal

def signal_handler(signal, frame):
    sys.exit(0)

signal.signal(signal.SIGINT, signal_handler)

HOST = '192.168.1.1'  # The server's hostname or IP address
HOST_PORT = 65433        # The port used by the server
CLIENT_PORT = 65432    #Local port
sockH = socket.socket(socket.AF_INET, socket.SOCK_DGRAM) #Host socket, remote
sockC = socket.socket(socket.AF_INET, socket.SOCK_DGRAM) #Client Socket, local

#Setup socket to receive nework connections
sockC.bind(("",CLIENT_PORT))

while(1):
    data, addr = sockC.recvfrom(1024)
    #print(data.decode())
    #When a request is received from the host, test the download speeds
    if (data.decode() == 'req'):
        #Sample number of packets received then wait 0.75 seconds
        dl=0.00
        t0 = time.time()
        download=psutil.net_io_counters(pernic=True)['Wi-Fi'][1]
        time.sleep(0.75)
        
        #Sample number of packets received 
        t1 = time.time()
        last_download = download
        download=psutil.net_io_counters(pernic=True)['Wi-Fi'][1]
        #Calclate the download speeds in kbps
        try:
            dl = (download - last_download) / (t1 - t0) / 1024.0             
        except:
            pass
        dl = dl*8 
        print('DL: {:0.2f} kbps'.format(dl))
        string = '{:0.2f}'.format(dl)
        message = bytes(string, 'utf-8')
        #Send download rate value to host
        sockH.sendto(message, (HOST,HOST_PORT))
