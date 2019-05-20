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
    
    new_vid_command = "raspivid -n -t 0 -fl -b 10000000 -fps " + str(fps) + " -h " + str(res_y) + " -w " + str(res_x) + " -o - | gst-launch-1.0 -v fdsrc ! h264parse ! rtph264pay config-interval=10 pt=96 ! udpsink host= " + str(ip_address) + " port= " + str(port_number) + " &"
    print("Starting stream with fps=" + str(fps) + " and resolution " + str(res_x) + " x " + str(res_y)) 
    os.system(new_vid_command)


def get_bandwidth():
    CLIENT_PORT=65432
    sockC=socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

    sockC.bind(("",CLIENT_PORT))

    while(1):
        data, addr = sockC.recvfrom(1024)
        total_str = data.decode()
        total = float(total_str)
        if (total_str == ""):
            continue
        else:
            break

    return total


def get_bandwidth_id(bandwidth):
    if(bandwidth < 6.0):
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


