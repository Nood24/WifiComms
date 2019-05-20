import socket
import threading
import time


class listener:
	def __init__(self, port):
		self.port = port
		self.address = None
		self.other = None              
		self.s = socket.socket()          
		self.s.bind(('', port))          
		
	
	def update_other(self, address):
		self.other = address
		
	def get_address(self):
		return self.address
	
	def read(self):
		self.s.listen(5)      
		print("listening", self.port)
		self.c, addr = self.s.accept()      
		print ('Got connection from', addr[0])
		self.address = addr[0]
		while True:
			time.sleep(1)
			if (self.other):
				self.c.send(str.encode(self.other)) 
				
			
			
if __name__ == "__main__":
	gimbal = listener(5556)
	station = listener(5555)
	g = threading.Thread(target = gimbal.read)
	g.start()
	s = threading.Thread(target = station.read)
	s.start()
	a = False
	b = False
	while True:
		if((not a)):
			add = gimbal.get_address()
			if (add):
				station.update_other(add)
				print("gimbal",add)
				a = True
		if((not b)):
			add = station.get_address()
			if (add):
				gimbal.update_other(add)
				print("station", add)
				b = True
		if(a and b):
			break
		time.sleep(1)
	
