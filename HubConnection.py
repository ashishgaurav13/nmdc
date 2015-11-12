import socket, re, threading
from constants import *
from utility import *

class HubConnection(threading.Thread):

    def __init__(self, hub, port, username, password):
        """
        Initialise thread, and create a TCP socket which connects to hub:port
        with specified username and password.
        """
        threading.Thread.__init__(self)
        self.s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.s.connect((hub, port))
        self.s.settimeout(2.0)
        self.username = username
        self.password = password

    def run(self):
        """
        The main function to run when this thread is started.
        """
        print "Starting DC SERVER TCP Port"
        self.talk()
        print "Exiting TCP"

    def auth(self):
        """
        Authorise the HubConnection by sending password.
        """
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
        """
        Start talking with the Hub by authorising and interactively going in
        a send receive loop.
        """
        self.auth()
        while True:
          isend(self.s)
          nbrecv(self.s)
