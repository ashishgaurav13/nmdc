import socket
from constants import *
from utility import *

class PlainTalk:

  def __init__(self, hub, username, password):
    # establish connection
    self.s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    self.s.connect((hub, PORT))
    self.s.settimeout(2.0)
    self.username = username
    self.password = password

  def auth(self):
    
    # first get the lock
    i = nbrecv(self.s)
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
