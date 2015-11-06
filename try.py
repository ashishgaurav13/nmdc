import socket
from constants import *
from utility import *

# establish connection
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect(('172.16.32.222', PORT))
s.settimeout(2.0)

# get initial message
recv(s)

# send validate stuff
send(s, "$Supports UserCommand UserIP2 TTHSearch|")
send(s, "$ValidateNick testBoy|")

# receive stuff
while True:
  try:
    recv(s)
  except:
    break

print "ENDING"
s.close()
