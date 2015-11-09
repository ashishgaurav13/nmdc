import socket
from constants import *
from utility import *
import re
import threading

class PlainTalk(threading.Thread):

    def __init__(self, hub, port, username, password):
        # establish connection
        threading.Thread.__init__(self)
        self.s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.s.connect((hub, port))
        self.s.settimeout(2.0)
        self.username = username
        self.password = password
    def run(self):
        print "Starting DC SERVER TCP Port"
        self.talk()
        print "Exiting TCP"
    def auth(self):

        # first get the lock
        i = nbrecv(self.s)
        j = i[0].split("|")
        m  = re.match('\$\w+',j[0])
        if m:
            print m.group(0)
            
        lock = i[0].split()[1]

        # send key and validate request
        send(self.s, '$Supports UserCommand UserIP2|')
        send(self.s, '$Key '+key(lock)+'|')
        send(self.s, '$ValidateNick '+self.username+'|')

        # get the GetPass request (TODO:add an assert here)
        nbrecv(self.s)

        # send the password
        send(self.s, '$MyPass '+self.password+'|')

        # get Hello
        nbrecv(self.s)

        # send some info about yourself
        send(self.s, '$Version 1,0091|')
        send(self.s, '$GetNickList|')
        send(self.s, '$MyINFO $ALL '+self.username+' $$$$$|')

        # get other stuff
        nbrecv(self.s)

    def talk(self):
        self.auth()
        while True:
          isend(self.s)
          nbrecv(self.s)

class PlainUDP(threading.Thread):
    """docstring for PlainUDP"""
    def __init__(self, ip, port):
        threading.Thread.__init__(self)
        self.ip = ip
        self.port = port
        self.s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM) # UDP

    def run(self):
        try:
            self.s.bind((self.ip, self.port))
            print "Listening on Port"+str(self.ip)+":"+str(self.port)
            self.listen()
        except socket.error,msg:
            print "Error::"+str(msg)

    def listen(self):
        while True:
                data, addr = self.s.recvfrom(1024) # buffer size is 1024 bytes
                print "received message:", data
    
    def close(self):
        print "Interrupt Received"
        self.s.close()
        