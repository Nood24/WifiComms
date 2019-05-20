import socket
from threading import *
import io
import time
import picamera
import subprocess

#Recieve works
def recieveFunction():

    IP = "192.168.1.225"
    PORT = 65433
    
    with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as sock:

        sock.bind(("",PORT))
        while (1):
            data, addr = sock.recvfrom(1024)
            print("Recieved data: " + data.decode())
           
def sendFunction():
    HOST = "192.168.1.70"                                    #Add the IP of the ground station here 
    PORT = 65432

    with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as sock:
        sock.sendto(b"Hello WiFlyers Ground",(HOST,PORT))
        while True:
            user_input = input("Enter input to send:") 
            sock.sendto(user_input.encode(),(HOST,PORT))


def sendVideoFunction():
    client_socket = socket.socket()
    client_socket.connect(('192.168.1.70',8000)) #Change my_server to true hostname
    
    connection = client_socket.makefile('wb')

    try:
        with picamera.PiCamer() as camera:
            camera.resolution = (640,480)
            camera.framerate = 24
            camera.start_preview()
            time.sleep(2)
            camera.start_recording(connection,format = 'h264')
            camera.wait_recording(60)
            camera.stop_recording()
    finally:
        connection.close()
        client_socket.close()
    
    print("Sending Video")
           
threadRecieve = Thread(target = recieveFunction)
threadSend = Thread(target = sendFunction)
threadSendVideo = Thread(target = sendVideoFunction)


threadRecieve.start()
threadSend.start()
threadSendVideo.start()

