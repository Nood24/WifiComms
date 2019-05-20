class listener:

    def __init__(self,port):
        self.address = None
        import socket
        self.s = socket.socket() 
        print('listening on', port)
        self.s.bind(('', port))
    
    def read(self):
        self.s.listen(5)
        c, addr = self.s.accept()
        print (addr[0])
        c.send(bytes('connected', 'utf-8'))
        c.close()
        self.s.close()
        self.address = addr[0]
        return self.address
