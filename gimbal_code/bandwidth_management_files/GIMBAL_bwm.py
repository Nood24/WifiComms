import iperf3 
import time
import os
import subprocess
#import bandwidth_management as bwm
import bwmFPVlib as bwm
from listen import listener
from threading import *
import socket

#gimbal_ip = ''


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

'''
threadGimbal = Thread(target=get_gimbal_ip)
threadGimbal.start()

GS_PORT=5585
l = listener(GS_PORT)
ip_address = l.read()
ip_address = "192.168.1.42"
'''

port_number = 5600

ip_address = "192.168.1.43" 
print("\n\n\nStarting the first stream...\n\n\n")
raspivid_command = "raspivid -n -t 0 -fl -b 10000000 -fps 30 -h 720 -w 1280 -o - | gst-launch-1.0 -v fdsrc ! h264parse ! rtph264pay config-interval=10 pt=96 ! udpsink host= " + str(ip_address) + " port=" + str(port_number) + " &"
os.system(raspivid_command)

state = [False, False, False, False, True]
count = 0
current_state = 4
new_state = 0

s=socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
s.bind(('0.0.0.0', 65432))
while(1):
    bw_id=''
    
   # if (gimbal_ip!=''):
   #     bwm.send_bandwidth(gimbal_ip, bandwidth)
    while(1):
         bw_id = int(s.recv(1024))
         print(bw_id)
         if(bw_id!=''):
             break
    
    current_state = getState(state)
    state, count, new_state = update_state(state, current_state, bw_id, count)
    print("count: " , str(count))
    print("current_state " + str(current_state))
    print("New state " + str(new_state))
    print(state)  
    
    if(bw_id==current_state):
        print("=================================================Bandwidth the same = " + str(bw_id))
        continue
    print(">>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>Changing Bandwidth = " + str(bw_id))
    if(bw_id==0):
        bwm.change_video_quality(20, 180, 320, ip_address, port_number)
    elif(bw_id==1):
        bwm.change_video_quality(20, 360, 640, ip_address, port_number)
    elif(bw_id==2):
        bwm.change_video_quality(25, 480, 720, ip_address, port_number)
    elif(bw_id==3):
        bwm.change_video_quality(30, 720, 1080, ip_address, port_number)
    else:
        bwm.change_video_quality(30, 1080, 1680, ip_address, port_number)
    #previous_id = bw_id

