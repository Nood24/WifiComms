class listener:

    def __init__(self,port):
        self.address = None
        import socket
        self.s = socket.socket() 
        print('listening on', port)
        self.s.bind(('', port))
    
    def read(self):
        self.s.listen(5)
        self.c, addr = self.s.accept()
        print (addr[0])
        self.address = addr[0]
        return self.address
    def send(self, data):
        if (self.c):
            self.c.send(str.encode(data))

