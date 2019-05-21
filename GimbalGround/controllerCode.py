import io
import socket
import time
import struct
import numpy as np
import threading
import socket 
import os   
'''
class connect:
	def __init__(self):
		self.drone = '192.168.1.1'
		self.address = None
		self.s = socket.socket()          
		port = 5555           
		self.port = 5555
		self.s.bind(('', port))          
		self.startup()
		
	def startup(self):         
		s = self.s
		self.s.connect((self.drone, self.port)) 
		while True: 
			value = s.recv(1024) 
			print ('Initial Handshake to Drone')
			self.address = bytes.decode(value)
			return self.address
			
	def send(self, data):
		if (self.address):
			print(data)
			#s.send(data) 


class gimball_video:

	def __init__(self):
		# Start a socket listening for connections on 0.0.0.0:8000 (0.0.0.0 means
		# all interfaces)
		self.server_socket = socket.socket()
		self.server_socket.bind(('0.0.0.0', 777))
		self.server_socket.listen(0)
		# Accept a single connection and make a file-like object out of it
		self.connection = self.server_socket.accept()[0].makefile('rb')

	def run(self):
		while True:
			try:
				while True:
					# Read the length of the image as a 32-bit unsigned int. If the
					# length is zero, quit the loop
					image_len = struct.unpack('<L', self.connection.read(struct.calcsize('<L')))[0]
					if not image_len:
						break
					# Construct a stream to hold the image data and read the image
					# data from the connection
					image_stream = io.BytesIO()
					image_stream.write(self.connection.read(image_len))
					# Rewind the stream, open it as an image with opencv and do some
					# processing on it
					image_stream.seek(0)
					#image = Image.open(image_stream)

					data = np.frombuffer(image_stream.getvalue(), dtype=np.uint8)
					imagedisp = cv2.imdecode(data, 1)

					cv2.imshow("Frame",imagedisp)
					cv2.waitKey(1)  #imshow will not output an image if you do not use waitKey
					#cv2.destroyAllWindows() #cleanup windows 
			finally:
				self.connection.close()
				self.server_socket.close()

'''
class Controller:
	def __init__(self):
		self.x = 0
		self.y = 0
		self.px = 0
		self.py = 0

	def main(self):
		print("In Main")
		from inputs import get_gamepad
		"""Just print out some event infomation when the gamepad is used."""
		while 1:
			events = get_gamepad()
			for event in events:
				if event.code == "ABS_RX":
					self.px = self.x
					self.x = event.state

				if event.code == "ABS_RY":
					self.py = self.y
					self.y = event.state

			print("Y", self.y, "X", self.x)

	def get_values(self):
		return self.x, self.y


def executeControl(c):
	print("here")
	while True:
		(x,y) = c.get_values
		s.send((x,y))
		time.sleep(60)

		
def run_GStream():
    os.system('gst-launch-1.0.exe udpsrc port=5600 ! application/x-rtp, payload=96 ! rtpjitterbuffer ! rtph264depay ! avdec_h264 ! fpsdisplaysink sync=false text-overlay=false')	   

if __name__ == "__main__":
	
	#s = connect()
	#v = gimball_video()
	c = Controller()
	video_receive = threading.Thread(target = run_GStream)
	video_receive.start()
	c.main()
	#v.run()

