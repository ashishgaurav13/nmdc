from HubConnection import *
import time

def main():
	hc = HubConnection("172.16.32.222", 411 , "testBoy", "12345")
	hc.daemon = True
	hc.start()
	while True:
		try:
			time.sleep(1)
		except KeyboardInterrupt:
			hc.udp.close()
			break

if __name__ == '__main__':
	main()
