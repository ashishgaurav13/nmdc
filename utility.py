from constants import *
import select

def send(s, msg):
  s.send(msg)
  print SENT+msg

def recv(s):
  msg = s.recv(BUFLEN)
  print RECV+msg
  return msg
