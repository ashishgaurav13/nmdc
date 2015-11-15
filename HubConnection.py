import socket, select, re, threading
from Constants import *
from CommandEncoder import *
from UDPConnection import *
from ClientConnection import *

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

# EXTRA
EXTRA = dict()
EXTRA['Find'] = 'Find <search terms>'
EXTRA['Show'] = 'Show'
EXTRA['ShowSearchResults'] = 'ShowSearchResults'
EXTRA['DownloadById'] = 'DownloadById <id>'
EXTRA['ClientConnection'] = 'ClientConnection <otherip> <otherport>'


class HubConnection(threading.Thread):

    def __init__(self, hub, port, username, password, udpip = '192.168.158.191', udpport = 5005):
        """
        Initialise thread, and create a TCP socket which connects to hub:port
        with specified username and password.
        """
        threading.Thread.__init__(self)
        self.s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.s.connect((hub, port))
        self.s.settimeout(1.5)
        self.username = username
        self.password = password
        self.ip = udpip
        self.udpport = 5005
        # The buffer which holds all commands we receive.
        self.buff = ""
        # Mutex lock for the buffer
        self.mutex = threading.Lock()
        # UDP socket for active searches
        self.udp = UDPConnection(udpip, udpport, self)
        self.udp.daemon = True
        self.udp.start()
        # last set of search results
        self.search = ''
        self.searchResults = dict()
        self.searchMutex = threading.Lock()

    def run(self):
        """
        The main function to run when this thread is started.
        """
        print ("" if not hasColor else Fore.YELLOW) + "Starting DC SERVER TCP Port" + ("" if not hasColor else Style.RESET_ALL)
        self.talk()
        print ("" if not hasColor else Fore.YELLOW) + "Exiting TCP" + ("" if not hasColor else Style.RESET_ALL)

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
            try:
                self.isend()
                self.nbrecv()
            except KeyboardInterrupt:
                print "Coming out..."
                break
            except:
                print "Something went wrong"
            else:
                pass

    def send(self, msg, log = False):
        """ Send a message using socket s, and log it. """
        if len(msg) <= 0: return
        msgs = [i for i in msg.split() if len(i) > 0]
        if len(msgs) > 0 and msgs[0] == 'ShowCommands':
            self.send('ShowCommands')
            for extra in EXTRA:
                print (Fore.YELLOW if hasColor else "")+EXTRA[extra]+(Style.RESET_ALL if hasColor else "")
        elif len(msgs) > 0 and msgs[0] == 'Command':
            if msgs[1] in EXTRA:
                print (Fore.YELLOW if hasColor else "")+EXTRA[msgs[1]]+(Style.RESET_ALL if hasColor else "")
            else:
                self.send('Command '+msgs[1])
        elif len(msgs) > 0 and msgs[0] == 'Find':
            self.send('Search '+self.ip+' '+str(self.udpport)+' F?T?0?1?'+'$'.join(msgs[1:]))
        elif len(msgs) > 0 and msgs[0] == 'DownloadById':
            num = int(msgs[1])
            self.searchMutex.acquire()
            cc = ClientConnection(self.username, self.ip, -1, True, dict(self.searchResults[num]))
            self.searchMutex.release()
            cc.start()
            self.searchMutex.acquire()
            self.s.send(FUNCTIONS['ConnectToMe'](*((self.searchResults[num]['nick'], self.ip, cc.port))))
            self.searchMutex.release()
            cc.join() 
        elif len(msgs) > 0 and msgs[0] == 'ConnectToMe':
            cc = ClientConnection(self.username, msgs[2], -1, True)
            cc.start()
            self.s.send(FUNCTIONS[msgs[0]](*((msgs[1], msgs[2], cc.port))))
            cc.join()
        elif len(msgs) > 0 and msgs[0] in FUNCTIONS:
            resp = FUNCTIONS[msgs[0]](*(tuple(msgs[1:])))
            if resp: self.s.send(resp)
            # if a search, clear search results, they're going to be repopulated !!
            if 'Search' in msgs[0]:
                self.search = msgs[3].strip()
                self.searchMutex.acquire()
                self.searchResults = dict()
                self.searchMutex.release()
        elif len(msgs) > 0 and msgs[0] == 'Show':
            self.show()
        elif len(msgs) > 0 and msgs[0] == 'ShowSearchResults':
            self.showSearchResults()
        elif len(msgs) > 0 and msgs[0] == 'ClientConnection':
            # This is the part where the main loop halts and we enter a client connection loop (passive)
            cc = ClientConnection(self.username, msgs[1], int(msgs[2]))
            cc.start()
            cc.join()
        else:
            self.s.send('$'+msg+'|')
        if log:
            print (SENT if not hasColor else Fore.GREEN) + msg + ("" if not hasColor else Style.RESET_ALL)

    def isend(self):
        """ interactive send """
        msg = raw_input(SENT if not hasColor else "").strip()
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
        self.buff = Utility.formatAndShowBuff(self)
        self.mutex.release()

    def showSearchResults(self):
        self.searchMutex.acquire()
        for key in self.searchResults:
            print str(key)+': '+' ( around '+Utility.toMB(self.searchResults[key]['size'])+' MB - '+self.searchResults[key]['nick']+')\n'+self.searchResults[key]['filename']
        self.searchMutex.release()
