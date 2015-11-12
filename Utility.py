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

def formatCommand(cmd):
    """ Format Commands even more """
    ret = ''
    if len(cmd) > 0 and ' ' in cmd:
        ret += cmd[:cmd.find(' ')]
        cmd = cmd[cmd.find(' '):].strip()
        if '$$' in cmd:
            params = cmd.split('$$')
        else:
            params = cmd.split()
        ret += '\n\t'+'\n\t'.join(params)
    else:
        return cmd
    return ret
    
    
def formatSearchResult(sr):
    """ Format a search result so that it's correctly picked up by formatAndShowBuff """
    return sr.replace(chr(5), '$$')    
    
def formatAndShowBuff(hubConnection, unformatted = True, ignore = True):
    """ Format and Show a buffer, with the option to show unformatted messages and ignore info, quit and hello messages. """
    buff = hubConnection.buff
    while '|' in buff:
        dollarpos = buff.find('$')
        pipepos = buff.find('|')
        if pipepos == -1 or dollarpos == -1: 
            return
        if pipepos < dollarpos:
            if unformatted and not (('Quit' in buff[:pipepos]) or ('Hello' in buff[:pipepos]) or ('MyINFO' in buff[:pipepos])):
                print Fore.RED + buff[:pipepos] + Style.RESET_ALL
            buff = buff[pipepos+1:]
        else:
            if pipepos-dollarpos+1 > 0 and not (('Quit' in buff[dollarpos+1:pipepos]) or ('Hello' in buff[dollarpos+1:pipepos]) or ('MyINFO' in buff[dollarpos+1:pipepos])):
                if 'SR' in buff[dollarpos+1:pipepos] and chr(5) in buff[dollarpos+1:pipepos]:
                    try:
                        # It's a search result
                        sr = formatSearchResult(buff[dollarpos+1:pipepos]).split('$$')
                        srdict = dict()
                        # find first space and remove $SR
                        sr[0] = sr[0][sr[0].find(' ')+1:]
                        srdict['nick'] = sr[0][:sr[0].find(' ')].strip()
                        # remove nick now
                        sr[0] = sr[0][sr[0].find(' ')+1:]
                        srdict['filename'] = sr[0].strip()
                        # in sr[1], the format is filesize<space>slots
                        sr[1] = sr[1].split()
                        srdict['size'] = sr[1][0]
                        srdict['slots'] = sr[1][1]
                        # TODO : More info in sr[2], get it when needed
                        # size is a number
                        x = int(srdict['size'])
                    except:
                        pass
                    else:
                        hubConnection.searchMutex.acquire()
                        hubConnection.searchResults.append(srdict)
                        hubConnection.searchMutex.release()
                    print Fore.BLUE + formatCommand(formatSearchResult(buff[dollarpos+1:pipepos])).expandtabs(2) + Style.RESET_ALL
                else:
                    print Fore.BLUE + formatCommand(buff[dollarpos+1:pipepos]).expandtabs(2) + Style.RESET_ALL
            buff = buff[pipepos+1:]
    return buff
