from HubConnection import *
from UDPConnection import *
import time

def main():
	hc = HubConnection("172.16.32.222", 411 , "testBoy", "12345")
	hc.daemon = True
	hc.start()
	uc = UDPConnection("192.168.158.191", 5005)
	uc.daemon = True
	uc.start()
	while True:
		try:
			time.sleep(1)
		except KeyboardInterrupt:
			uc.close()
			break

if __name__ == '__main__':
	main()
