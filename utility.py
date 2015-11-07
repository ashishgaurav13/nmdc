from constants import *
import select
import socket

# Send a message using socket s, and log it.
def send(s, msg):
  s.send(msg)
  print SENT+msg

# interactive send
def isend(s):
  msg = raw_input(SENT).strip()
  s.send(msg)

# Receive a message from socket s, and log it.
def recv(s):
  msg = s.recv(BUFLEN)
  print RECV+msg
  return msg

# Non Blocking Receive
def nbrecv(s):
  ret = []
  while True:
    try:
      msg = s.recv(BUFLEN)
      if len(msg) <= 0: raise Exception
      print RECV+msg
      ret.append(msg)
    except:
      break
  return ret

# Create the key for a given lock
def key(lock):
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
