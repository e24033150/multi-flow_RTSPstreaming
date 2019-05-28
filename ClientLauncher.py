import sys
#from tkinter import Tk
try:
        from tkinter import Tk

except:
        from Tkinter import Tk


from Client import Client

if __name__ == "__main__":
	try:
		serverAddr = sys.argv[1]
		serverPort = sys.argv[2]
		rtpPort = sys.argv[3]
		fileName = sys.argv[4]	
		flow_num = sys.argv[5]
	except:
		print ("[Usage: ClientLauncher.py Server_name Server_port RTP_port Video_file]\n")	
	
	root = Tk()
	
	# Create a new client
	app = Client(root, serverAddr, serverPort, rtpPort, fileName, flow_num)
	app.master.title("RTPClient")	
	root.mainloop()
	
