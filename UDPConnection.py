import threading, socket

class UDPConnection(threading.Thread):

    def __init__(self, ip, port):
        """
        Initialise thread, and start a datagram (UDP) socket.
        """
        threading.Thread.__init__(self)
        self.ip = ip
        self.port = port
        self.s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM) # UDP

    def run(self):
        """
        Bind to specified ip and port, and listen for a connection
        """
        try:
            self.s.bind((self.ip, self.port))
            print "Listening on Port "+str(self.ip)+":"+str(self.port)
            self.listen()
        except socket.error,msg:
            print "Error:"+str(msg)

    def listen(self):
        """
        Show the data received.
        """
        while True:
                data, addr = self.s.recvfrom(1024) # buffer size is 1024 bytes
                print "U: ", data
    
    def close(self):
        """
        Close the socket.
        """
        print "Interrupt Received"
        self.s.close()
