import select, socket
from Constants import *

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


def key(lock):
    """ Create the key for a given lock """
    size = len(lock)
    x = chr(ord(lock[0])^ord(lock[size-1])^ord(lock[size-2])^5)
    for i in range(1, size): x += chr(ord(lock[i])^ord(lock[i-1]))
    for i in range(size): x = x[:i]+chr(((ord(x[i])<<4)&240)|((ord(x[i])>>4)&15))+x[i+1:]
    x = x.replace(chr(0),   '/%DCN000%/')\
       .replace(chr(5),   '/%DCN005%/')\
       .replace(chr(36),  '/%DCN036%/')\
       .replace(chr(96),  '/%DCN096%/')\
       .replace(chr(124), '/%DCN124%/')\
       .replace(chr(126), '/%DCN126%/')
    return x
    
def formatAndShowBuff(buff, unformatted = True):
    """ Format and Show a buffer, with the option to show unformatted messages. """
    while '|' in buff:
        dollarpos = buff.find('$')
        pipepos = buff.find('|')
        if pipepos == -1 or dollarpos == -1: 
            return
        if pipepos > dollarpos:
            if unformatted:
                print "<Unformatted>"
                print Fore.BLUE + buff[:pipepos] + Style.RESET_ALL
            buff = buff[pipepos+1:]
        else:
            if pipepos-dollarpos+1 > 0:
                print Fore.BLUE + buff[dollarpos+1:pipepos] + Style.RESET_ALL
            buff = buff[pipepos+1:]
    return buff
