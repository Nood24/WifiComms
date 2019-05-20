import iperf3
import time
import os
import subprocess
import socket

def change_video_quality(fps, res_x, res_y, ip_address, port_number):
    print("Killing first stream...")
    pid = subprocess.check_output("pidof raspivid", shell=True)
    print("PID BELOW VVVV")
    pid_int = int(pid)
    print(pid_int)
    st = "kill " + str(pid_int)
    os.system(st)
    
    new_vid_command = "raspivid -n -vf -t 0 -fl -b 10000000 -fps " + str(fps) + " -h " + str(res_y) + " -w " + str(res_x) + " -o - | gst-launch-1.0 -v fdsrc ! h264parse ! rtph264pay config-interval=10 pt=96 ! udpsink host= " + str(ip_address) + " port= " + str(port_number) + " &"
    print("Starting stream with fps=" + str(fps) + " and resolution " + str(res_x) + " x " + str(res_y)) 
    os.system(new_vid_command)


def get_bandwidth(ip_address):
    CLIENT_PORT=65432
    HOST_PORT=65433
    sockH=socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sockC=socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

    sockH.bind(("",HOST_PORT))

    sockC.sendto(b'req',(ip_address,CLIENT_PORT))
    while(1):
        data, addr = sockH.recvfrom(1024)
        dl_str = data.decode()
        DL = float(dl_str)/1000
        if (dl_str == ""):
            continue
        else:
            break

    client = iperf3.Client()
    print(ip_address)
    client.duration = 1
    client.server_hostname = str(ip_address)
    client.port = 5201  # parameterise?
    client.protocol = 'udp' 
    result = client.run()
    bandwidth = result.Mbps
    #bandwidth = result.sent_Mbps
    total = bandwidth + DL
    return total


def get_bandwidth_id(bandwidth):
    if(bandwidth < 6.0 or bandwidth > 80):
        bw_id = 0
    elif(bandwidth < 12.0):
        bw_id = 1
    elif(bandwidth < 18.0):
        bw_id = 2
    elif(bandwidth < 24.0):
        bw_id = 3
    else:
        bw_id = 4
    return bw_id

def send_bandwidth(ip_address, bw_id ):

    CLIENT_PORT=65432
    sock=socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    b_str = str(bw_id)
    #b_str = '{:0.4f}'.format(bandwidth)
    message = bytes(b_str, 'utf-8')
    sock.sendto(message,(ip_address,CLIENT_PORT))

