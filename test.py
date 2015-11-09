from PlainTalk import *
import time
def main():
	pt = PlainTalk("172.16.32.222",411 , "testBoy", "12345")
	pt.daemon = True
	pt.start()
	pu = PlainUDP("192.168.106.203",5005)
	pu.daemon = True
	pu.start()
	while True:
		try:
			time.sleep(1)
		except KeyboardInterrupt:
			pu.close()
			break

if __name__ == '__main__':
	main()
