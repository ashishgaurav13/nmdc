import socket, select, re, threading
from Constants import *
from CommandEncoder import *

hasColor = False
# import colorama if it exists
try: 
    import colorama
except: 
    pass
else: 
    from colorama import Fore, Style 
    colorama.init()
    hasColor = True


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
        # The buffer which holds all commands we receive.
        self.buff = ""
        # Mutex lock for the buffer
        self.mutex = threading.Lock()

    def run(self):
        """
        The main function to run when this thread is started.
        """
        print (Fore.YELLOW if hasColor else "") + "Starting DC SERVER TCP Port" + (Style.RESET_ALL if hasColor else "")
        self.talk()
        print (Fore.YELLOW if hasColor else "") + "Exiting TCP" + (Style.RESET_ALL if hasColor else "")

    def auth(self):
        """
        Authorise the HubConnection by sending password.
        """
        # first get the lock
        i = self.nbrecv(log = True)
        j = i[0].split("|")
        lock = i[0].split()[1]
        # send key and validate request
        self.send('Supports UserCommand UserIP2', log = True)
        self.send('Key '+lock, log = True)
        self.send('ValidateNick '+self.username, log = True)
        # get the GetPass request (TODO:add an assert here)
        self.nbrecv(log = True)
        # send the password
        self.send('MyPass '+self.password)
        print "MyPass ***"
        # get Hello
        self.nbrecv(log = True)
        # send some info about yourself
        self.send('Version 1,0091', log = True)
        self.send('GetNickList', log = True)
        self.send('MyINFO '+self.username, log = True)
        # get other stuff
        self.nbrecv(log = True)

    def talk(self):
        """
        Start talking with the Hub by authorising and interactively going in
        a send receive loop.
        """
        self.auth()
        while True:
            self.isend()
            self.nbrecv()

    def send(self, msg, log = False):
        """ Send a message using socket s, and log it. """
        if len(msg) <= 0: return
        msgs = [i for i in msg.split() if len(i) > 0]
        if len(msgs) > 0 and msgs[0] in FUNCTIONS:
            resp = FUNCTIONS[msgs[0]](*(tuple(msgs[1:])))
            if resp: self.s.send(resp)
        elif len(msgs) > 0 and msgs[0] == 'Show':
            self.show()
        else:
            self.s.send('$'+msg+'|')
        if log:
            print (Fore.GREEN if hasColor else SENT) + msg + (Style.RESET_ALL if hasColor else "")

    def isend(self):
        """ interactive send """
        msg = raw_input(SENT).strip()
        self.send(msg)

    def recv(self, log = False):
        """ Receive a message from socket s, and log it. """
        msg = self.s.recv(BUFLEN)
        self.mutex.acquire()
        self.buff += msg
        self.mutex.release()
        if log:
            self.show()
        return msg

    def nbrecv(self, log = False):
        """ Non Blocking Receive """
        ret = []
        while True:
            try:
                msg = self.s.recv(BUFLEN)
                if len(msg) <= 0: raise Exception
                self.mutex.acquire()
                self.buff += msg
                self.mutex.release()
                ret.append(msg)
            except:
                break
        if log:
            self.show()
        return ret
        
    def show(self):
        """ Show previous commands and messages. """
        self.mutex.acquire()
        self.buff = Utility.formatAndShowBuff(self.buff)
        self.mutex.release()

