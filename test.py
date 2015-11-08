from PlainTalk import *

def main():
	pt = PlainTalk("172.16.32.222",411 , "testBoy", "12345")
	pt.start()
	pu = PlainUDP("192.168.106.203",5000)
	pu.start()

if __name__ == '__main__':
	main()
