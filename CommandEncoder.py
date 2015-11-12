import Utility

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


""" All the functions """
FUNCTIONS = dict()

def chat(nick, message):
    """ Chat <nick> <message> """ 
    return "<%s> %s|" % (nick, message)

FUNCTIONS['Chat'] = chat

def to(othernick, nick, message): 
    """ To <othernick> <nick> <message> """
    return "$To: %s From: %s <%s> %s|" % (othernick, nick, nick, message)

FUNCTIONS['To'] = to

def connectToMe(remotenick, senderip, senderport):
    """ ConnectToMe <remotenick> <senderip> <senderport> """
    return "$ConnectToMe %s %s:%s|" % (remotenick, senderip, senderport)

FUNCTIONS['ConnectToMe'] = connectToMe

def connectToMe2(sendernick, remotenick, senderip, senderport):
    """ ConnectToMe2 <sendernick> <remotenick> <senderip> <senderport> """
    return "$ConnectToMe %s %s %s:%s|" % (sendernick, remotenick, senderip, senderport)

FUNCTIONS['ConnectToMe2'] = connectToMe2

def revConnectToMe(sendernick, remotenick):
    """ RevConnectToMe <sendernick> <remotenick> """
    return "$RevConnectToMe %s %s|" % (sendernick, remotenick)

FUNCTIONS['RevConnectToMe'] = revConnectToMe

def ping(senderip, senderport):
    """ Ping <senderip> <senderport> """
    return "$Ping %s:%s|" % (senderip, senderport)

FUNCTIONS['Ping'] = ping

def getPass():
    """ GetPass """
    return "$GetPass|"

FUNCTIONS['GetPass'] = getPass

def myPass(password):
    """ MyPass <password> """
    return "$MyPass %s|" % (password)

FUNCTIONS['MyPass'] = myPass

def logedIn(nick):
    """ LogedIn <nick> ; not a typo !! """
    return "$LogenIn %s|" % (nick)

FUNCTIONS['LogedIn'] = logedIn

def get(filename, offset):
    """ Get <file> <offset> """
    return "$Get %s$%s|" % (filename, offset)

FUNCTIONS['Get'] = get

def send():
    """ Send """
    return "$Send|"

FUNCTIONS['Send'] = send

def fileLength(filesize):
    """ FileLength <filesize> """
    return "$FileLength %s|" % (filesize)

FUNCTIONS['FileLength'] = fileLength

def getListLen():
    """ GetListLen """
    return "$GetListLen|"

FUNCTIONS['GetListLen'] = getListLen

def listLen(filesize):
    """ ListLen <filesize> """
    return "$ListLen %s|" % (filesize)

FUNCTIONS['ListLen'] = listLen

def direction(direction, number):
    """ Direction <direction> <number> """
    return "$Direction %s %s|" % (direction, number)

FUNCTIONS['Direction'] = direction

def cancel():
    """ Cancel """
    return "$Cancel|"

FUNCTIONS['Cancel'] = cancel

def canceled():
    """ Canceled """
    return "$Canceled|"

FUNCTIONS['Canceled'] = canceled

def badPass():
    """ BadPass """
    return "$BadPass|"

FUNCTIONS['BadPass'] = badPass

def hubIsFull():
    """ HubIsFull """
    return "$HubIsFull|"

FUNCTIONS['HubIsFull'] = hubIsFull

def validateDenide(nick):
    """ ValidateDenide <nick> """
    return "$ValidateDenide %s|" % (nick)

FUNCTIONS['ValidateDenide'] = validateDenide

def maxedOut():
    """ MaxedOut """
    return "$MaxedOut|"

FUNCTIONS['MaxedOut'] = maxedOut

def failed(message):
    """ Failed <message> """
    return "$Failed %s|" % (message)

FUNCTIONS['Failed'] = failed

def error(message):
    """ Error <message> """
    return "$Error %s|" % (message)

FUNCTIONS['Error'] = error

def search(ip, port, searchstring):
    """ Search <ip> <port> <searchstring> """
    return "$Search %s:%s %s|" % (ip, port, searchstring)

FUNCTIONS['Search'] = search

# TODO : search results ??

def myINFO(nick, description = '', connection = '', flag = '', mail = '', sharesize = '0'):
    """ MyINFO <nick> <description> <connection> <flag> <mail> <sharesize> """
    return "$MyINFO $ALL %s %s $$%s%s$%s$%s$|" % (nick, description, connection, flag, mail, sharesize)

FUNCTIONS['MyINFO'] = myINFO

def getINFO(othernick, nick):
    """ GetINFO <othernick> <nick> """
    return "$GetINFO %s %s|" % (othernick, nick)

FUNCTIONS['GetINFO'] = getINFO

def hello(nick):
    """ Hello <nick> """
    return "$Hello %s|" % (nick)

FUNCTIONS['Hello'] = hello

def version(version):
    """ Version <version> """
    return "$Version %s|" % (version)

FUNCTIONS['Version'] = version

def hubName(name):
    """ HubName <name> """
    return "$HubName %s|" % (name)

FUNCTIONS['HubName'] = hubName

def getNickList():
    """ GetNickList """
    return "$GetNickList|"

FUNCTIONS['GetNickList'] = getNickList

def nickList(*nickarray):
    """ NickList <nick1> <nick2> ... """
    return "$NickList "+('$$'.join(nickarray))+"|"

FUNCTIONS['NickList'] = nickList

def opList(*oparray):
    """ OpList <op1> <op2> ... """
    return "$OpList "+('$$'.join(oparray))+"|"

FUNCTIONS['OpList'] = opList

def kick(victim):
    """ Kick <victim> """
    return "$Kick %s|" % (victim)

FUNCTIONS['Kick'] = kick

def close(victim):
    """ Close <victim> """
    return "$Close %s|" % (victim)

FUNCTIONS['Close'] = close

def opForceMove(victim, address, reason):
    """ OpForceMove <victim> <address> <reason> """
    return "$OpForceMove $Who:%s$Where:%s$Msg:%s|" % (victim, address, reason)

FUNCTIONS['OpForceMove'] = opForceMove

def forceMove(address):
    """ ForceMove <address> """
    return "$ForceMove %s|" % (address)

FUNCTIONS['ForceMove'] = forceMove

def quit2(nick):
    """ Quit <nick> """
    return "$Quit %s|" % (nick)

# Python already has a quit
FUNCTIONS['Quit'] = quit2

def lock(lock, pk):
    """ Lock <lock> <pk>"""
    return "$Lock %s Pk=%s|" % (lock, pk)

FUNCTIONS['Lock'] = lock

def key(lock):
    """ Key <lock> """
    return "$Key %s|" % (Utility.key(lock))

FUNCTIONS['Key'] = key

def multiConnectToMe(remotenick, senderip, senderport):
    """ MultiConnectToMe <remotenick> <senderip> <senderport> """
    return "$MultiConnectToMe %s %s:%s|" % (remotenick, senderip, senderport)

FUNCTIONS['MultiConnectToMe'] = multiConnectToMe

def multiSearch(ip, port, searchstring):
    """ MultiSearch <ip> <port> <searchstring> """
    return "$MultiSearch %s:%s %s|" % (ip, port, searchstring)

FUNCTIONS['MultiSearch'] = multiSearch

def supports(*whatever):
    """ Supports <arg1> <arg2> ... """
    return "$Supports "+(' '.join(whatever))+"|"

FUNCTIONS['Supports'] = supports

#  Help functions

def command(commandname):
    """ Command <commandname> """
    if commandname in FUNCTIONS:
        print (Fore.YELLOW if hasColor else "") + FUNCTIONS[commandname].__doc__ + (Style.RESET_ALL if hasColor else "")
    else:
        print (Fore.YELLOW if hasColor else "") + "Not found." + (Style.RESET_ALL if hasColor else "")

FUNCTIONS['Command'] = command

def showCommands():
    """ ShowCommands """
    for key in FUNCTIONS:
        command(key)

FUNCTIONS['ShowCommands'] = showCommands
