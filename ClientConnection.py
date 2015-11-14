import socket, select, re, threading, random, zlib, bz2
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


class ClientConnection(threading.Thread):
    """ We don't need a TCP Server Socket, that must be provided, we're the client downloading side. """

    def __init__(self, nick, ip, port, listen = False):
        """
        Initialise thread, and create a TCP socket which connects to ip:port which you would
        have when you did the RevConnectToMe thing.
        """
        threading.Thread.__init__(self)
        self.listen = listen
        self.s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        if listen:
            while True:
                # try getting a port
                self.port = int(random.random()*10000)
                try:
                    self.s.bind((ip, self.port))
                except:
                    continue
                else:
                    break
            self.s.listen(1)
        else:
            self.port = port
            self.s.connect((ip, port))
            self.s.settimeout(1.5)
        # The buffer which holds all commands we receive.
        self.buff = ""
        # Mutex lock for the buffer
        self.mutex = threading.Lock()
        # is the connection active?
        self.isActive = True
        self.username = nick

    def run(self):
        """
        The main function to run when this thread is started.
        """
        print ("" if not hasColor else Fore.YELLOW) + "Entering Client Communication Mode" + ("" if not hasColor else Style.RESET_ALL)
        if self.listen:
            # wait for something to connect
            self.conn, self.clientAddress = self.s.accept()
            print ("" if not hasColor else Fore.YELLOW) + "Connected to " + str(self.clientAddress) + ("" if not hasColor else Style.RESET_ALL) 
            self.conn, self.s = self.s, self.conn
            self.s.settimeout(1.5)
        self.talk()n
        print ("" if not hasColor else Fore.YELLOW) + "Exiting Client Communication Mode" + ("" if not hasColor else Style.RESET_ALL)

    def auth(self):
        """
        Authorise the ClientConnection by sending password.
        """
        if self.listen:
            # Get the MyNick message and Lock Message, because you sent ConnectToMe
            r = []
            while len(r) <= 0: r = self.nbrecv(log = True)
            r = ''.join([s.replace('|', '|^') for s in r]).split('^')
            # Send the same lock, and the send the key you get
            lock = r[1].split()[1]
            self.send("MyNick "+self.username, log = True)
            self.send("Lock "+lock+" DCPLUSPLUS0.706ABCABC", log = True) # For now
            # Get all messages
            r = self.nbrecv(log = True)
            r = ''.join([s.replace('|', '|^') for s in r]).split('^')
            self.send("Supports MiniSlots XmlBZList ADCGet TTHL TTHF ZLIG", log = True)
            self.send("Direction Download 50000", log = True)
            self.send(r[2]+'IGNORE' if 'Key' in r[2] else "Key "+lock)
            
        
    def downloadFile(self, filename):
        """
        Once connected, download the file and save it as filename.
        """
        filetype = "tthl" if "TTH/" in filename else "file"
        self.send("ADCGET "+filetype+" "+filename+" 0 -1 ZL1")
        st = ''
        try:
            st += ''.join(self.nbrecv(log = False))
            self.mutex.acquire()
            self.buff = ''
            self.mutex.release() 
        except:
            pass
        st = st[st.find('|')+1:]
        print len(st)
        f = open(filename.replace('TTH/', ''), 'w')
        f.write(st)
        f.close()
        print ("" if not hasColor else Fore.YELLOW) + "File (compressed)" + filename + " was downloaded. Check the folder!" + ("" if not hasColor else Style.RESET_ALL)
        
    def talk(self):
        """
        Start talking with the Hub by authorising and interactively going in
        a send receive loop.
        """
        self.auth()
        while self.isActive:
            self.isend()
            self.nbrecv()

    def send(self, msg, log = False):
        """ Send a message using socket s, and log it. """
        if len(msg) <= 0: return
        msgs = [i for i in msg.split() if len(i) > 0]
        if 'IGNORE' in msg:
            self.s.send(msg.replace('IGNORE', ''))
        elif len(msgs) > 0 and msgs[0] in FUNCTIONS:
            resp = FUNCTIONS[msgs[0]](*(tuple(msgs[1:])))
            if resp: self.s.send(resp)
        elif len(msgs) > 0 and msgs[0] == 'Download':
            self.downloadFile(''.join(msgs[1:]))
        elif len(msgs) > 0 and msgs[0] == 'Show':
            self.show()
        elif len(msgs) > 0 and msgs[0] == 'Exit':
            self.isActive = False
        else:
            self.s.send('$'+msg+'|')
        if log:
            print (SENT if not hasColor else Fore.GREEN) + msg.replace('IGNORE', '') + ("" if not hasColor else Style.RESET_ALL)

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
