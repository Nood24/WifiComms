import iperf3 
import time
import os
import subprocess
#import bandwidth_management as bwm
import bwmFPVlib as bwm
from listen import listener
from threading import *


gimbal_ip = '192.168.1.18'


def update_state(state, current, new_state, count): 
    if new_state != current:
        count += 1

    # moving down
    if new_state < current:
        state[current] = False
        state[new_state] = True
        current_state  = new_state
        count = 0
    elif count > 2:
        state[current] = False
        current = current + 1 
        state[current] = True
        count = 0
    return state, count, new_state


def getState(state):
    i = 0
    while i < len(state):
        if state[i] == True:
           return i
        i+=1
    print("An error has occurred no state exists")
    return -1

        

def get_gimbal_ip():
    global gimbal_ip
    GIMBAL_PORT=5584
    
    l=listener(GIMBAL_PORT)
    ip_address = l.read()
    gimbal_ip = ip_address

threadGimbal = Thread(target=get_gimbal_ip)
threadGimbal.start()

GS_PORT=5585
l = listener(GS_PORT)
ip_address = l.read()

port_number = 5600

 
print("\n\n\nStarting the first stream...\n\n\n")
raspivid_command = "raspivid -n -vf -t 0 -fl -b 10000000 -fps 30 -h 720 -w 1280 -o - | gst-launch-1.0 -v fdsrc ! h264parse ! rtph264pay config-interval=10 pt=96 ! udpsink host= " + str(ip_address) + " port=" + str(port_number) + " &"
os.system(raspivid_command)

state = [False, False, False, False, True]
count = 0
current_state = 4
new_state = 0

mavString = "sudo mavproxy.py --master=/dev/ttys0 --baudrate 57600 --out " + ip_address + ":14550 --aircraft MyCopter"

os.system()

while(1):
    
    # how often it polls
    time.sleep(5)
    bandwidth = bwm.get_bandwidth(ip_address)
    bw_id = bwm.get_bandwidth_id(bandwidth)
    if (gimbal_ip!=''):       
        bwm.send_bandwidth(gimbal_ip, bw_id)

    
    current_state = getState(state)
    state, count, new_state = update_state(state, current_state, bw_id, count)
    print("count: " , str(count))
    print("current_state " + str(current_state))
    print("New state " + str(new_state))
    print(state)  
    
    if(bw_id==current_state):
        print("=================================================Bandwidth the same = " + str(bandwidth))
        continue
    print(">>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>Changing Bandwidth = " + str(bandwidth))
    if(bw_id==0):
        bwm.change_video_quality(20, 180, 270, ip_address, port_number)
    elif(bw_id==1):
        bwm.change_video_quality(20, 360, 540, ip_address, port_number)
    elif(bw_id==2):
        bwm.change_video_quality(25, 480, 720, ip_address, port_number)
    elif(bw_id==3):
        bwm.change_video_quality(30, 720, 1280, ip_address, port_number)
    else:
        bwm.change_video_quality(30, 720, 1280, ip_address, port_number)
    #previous_id = bw_id

