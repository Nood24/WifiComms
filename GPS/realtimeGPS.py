'''
Get realtime GPS data from a specified UDP port and send to a receiver.
Need to specify a seperate '--out' address when running mavproxy.
eg. "maxproxy.exe ... --out 127.0.0.1:14551"
Then run "python realtimeGPS.py --connect 127.0.0.1:14551"
'''


from __future__ import print_function
from dronekit import connect, VehicleMode
from pymavlink import mavutil
import argparse  
import time
import socket
import sys

# send a string to the given IP Address and Port
def send(gps_string):
    DEST_IP = '192.168.1.13'  # Static Address for GPS receiver. Always 192.168.1.150
    PORT    = 4210        # The port used by the receiver. Always 0x2616

    with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as s:
        s.sendto(gps_string.encode(), (DEST_IP, PORT))


#Set up option parsing to get connection string
parser = argparse.ArgumentParser(description='Connects to SITL on local PC by default.')
parser.add_argument('--connect',
                   help="vehicle connection target: IP_ADDRESS:HOST")
args = parser.parse_args()
connection_string = args.connect # get the connect argument
sitl = None

#Start SITL if no connection string specified
if not connection_string:
    import dronekit_sitl
    sitl = dronekit_sitl.start_default()
    connection_string = sitl.connection_string()

# Connect to the Vehicle
print('Connecting to vehicle on: %s' % connection_string)
vehicle = connect(connection_string)

#vehicle.wait_ready('autopilot_version')
# send GPS data every second
gps_string = ""
try:
    while (1):
        # split to leave just the data

        gpsData = str(vehicle.location.global_frame).split(':')[1].split(',')
        gpsData[0] = gpsData[0].replace("lat=","")
        gpsData[0] = gpsData[0].replace("." , "")
        gpsData[0] = gpsData[0] + 't'
        gpsData[1] = gpsData[1].replace("lon=","")
        gpsData[1] = gpsData[1].replace(".", "")
        gpsData[1] = gpsData[0] + 'n'
        gpsData[2] = gpsData[2].replace("alt=","")
        gpsData[2] = gpsData[2].replace(".", "")
        gpsData[2] = gpsData[2] + 'a'
        gps_string = ' '.join(gpsData)
        print(gps_string)
        send(gps_string)
       # file.write(gpsData)

       # print(str(vehicle.location.global_frame).split(':')[1])
       # send(str(vehicle.location.global_frame).split(':')[1])
        time.sleep(1)

except KeyboardInterrupt:
    print("Interrupted")
    sys.exit(0)

