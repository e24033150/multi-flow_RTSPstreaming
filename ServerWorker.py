from random import randint
import sys, traceback, threading, socket

from VideoStream import VideoStream
from RtpPacket import RtpPacket

### In general MTU
#data_size = 1458

### When MTU decreases by 50 bytes
data_size = 1408


class ServerWorker:
	SETUP = 'SETUP'
	PLAY = 'PLAY'
	PAUSE = 'PAUSE'
	TEARDOWN = 'TEARDOWN'
	
	INIT = 0
	READY = 1
	PLAYING = 2
	state = INIT

	OK_200 = 0
	FILE_NOT_FOUND_404 = 1
	CON_ERR_500 = 2
	
	clientInfo = {}
	
	def __init__(self, clientInfo):
		self.clientInfo = clientInfo
		self.frameNum = 0
		
	def run(self):
		threading.Thread(target=self.recvRtspRequest).start()
	
	def recvRtspRequest(self):
		"""Receive RTSP request from the client."""
		connSocket = self.clientInfo['rtspSocket'][0]
		while True:            
			data = connSocket.recv(256)
			if data:
				print ("DATA RECEIVED: \n", data)
				self.processRtspRequest(data.decode())
	
	def processRtspRequest(self, data):
		"""Process RTSP request sent from the client."""
		# Get the request type
		request = data.split('\n')
		line1 = request[0].split(' ')
		requestType = line1[0]
		
		# Get the media file name
		filename = line1[1]
		
		# Get the RTSP sequence number 
		seq = request[1].split(' ')
		
		# Process SETUP request
		if requestType == self.SETUP:
			if self.state == self.INIT:
				# Update state
				print ("PROCESSING SETUP\n")
				
				try:
					self.clientInfo['videoStream'] = VideoStream(filename)
					self.state = self.READY
				except IOError:
					self.replyRtsp(self.FILE_NOT_FOUND_404, seq[1])
				
				# Generate a randomized RTSP session ID
				self.clientInfo['session'] = randint(100000, 999999)
				
				# Send RTSP reply
				self.replyRtsp(self.OK_200, seq[1])
				
				# Get the RTP/UDP port from the last line
				self.clientInfo['rtpPort'] = request[2].split(' ')[3]

				# Get the flow_num from client request
				self.clientInfo['flow_num'] = int(request[2].split(' ')[5])
		# Process PLAY request 		
		elif requestType == self.PLAY:
			if self.state == self.READY:
				print ("PROCESSING PLAY\n")
				self.state = self.PLAYING
				
				# Create a new socket for RTP/UDP
				self.clientInfo["rtpSocket"] = [socket.socket(socket.AF_INET, socket.SOCK_DGRAM) for _ in range(self.clientInfo['flow_num'])]
				for i in range(self.clientInfo['flow_num']):
					server_address = ('',23456 + i)
					self.clientInfo["rtpSocket"][i].bind(server_address)

				self.replyRtsp(self.OK_200, seq[1])
				
				# Create a new thread and start sending RTP packets
				self.clientInfo['event'] = threading.Event()
				self.clientInfo['worker']= threading.Thread(target=self.sendRtp) 
				self.clientInfo['worker'].start()
		
		# Process PAUSE request
		elif requestType == self.PAUSE:
			if self.state == self.PLAYING:
				print ("PROCESSING P A U S E\n")
				self.state = self.READY
				
				self.clientInfo['event'].set()
			
				self.replyRtsp(self.OK_200, seq[1])
		
		# Process TEARDOWN request
		elif requestType == self.TEARDOWN:
			print ("PROCESSING TEARDOWN\n")

			self.clientInfo['event'].set()
			
			self.replyRtsp(self.OK_200, seq[1])
			
			# Close the RTP socket
			for i in range(self.clientInfo['flow_num']):
				self.clientInfo['rtpSocket'][i].close()
			#self.clientInfo['rtpSocket'].close()
			
	def sendRtp(self):
		"""Send RTP packets over UDP."""
		current_index = 0
		while True:
			self.clientInfo['event'].wait(0.015) 
			
			# Stop sending if request is PAUSE or TEARDOWN
			if self.clientInfo['event'].isSet(): 
				break 
				
			data = self.clientInfo['videoStream'].nextFrame()
			if data.any(): 
				#frameNumber = self.clientInfo['videoStream'].frameNbr()
				#frameNumber = self.frameNum
				data_bytes = data.tobytes()
				address = self.clientInfo['rtspSocket'][1][0]
				port = int(self.clientInfo['rtpPort'])


				if len(data_bytes) < data_size:
					try:
						self.frameNum += 1
						self.clientInfo['rtpSocket'][current_index].sendto(self.makeRtp(data_bytes, self.frameNum,1),(address,port))
					except:
						print (len(data_bytes))
						print ("Connection Error")
				else:
					try:
						times = int(len(data_bytes)//data_size)
						for i in range(times):
							self.frameNum += 1
							self.clientInfo['rtpSocket'][current_index].sendto(self.makeRtp(data_bytes[i*data_size:(i+1)*data_size], self.frameNum,0),(address,port))
						self.frameNum += 1
						self.clientInfo['rtpSocket'][current_index].sendto(self.makeRtp(data_bytes[times*data_size:], self.frameNum,1),(address,port))
					except:
						print (len(data_bytes))
						print ("Connection Error")
			current_index = (current_index + 1) % self.clientInfo['flow_num']

	def makeRtp(self, payload, seqnum, marker):
		"""RTP-packetize the video data."""
		version = 2
		padding = 0
		extension = 0
		cc = 0
		pt = 26 # MJPEG type
		ssrc = 0 
		
		rtpPacket = RtpPacket()
		
		rtpPacket.encode(version, padding, extension, cc, seqnum, marker, pt, ssrc, payload)
		
		return rtpPacket.getPacket()
		
	def replyRtsp(self, code, seq):
		"""Send RTSP reply to the client."""
		if code == self.OK_200:
			#print "200 OK"
			reply = 'RTSP/1.0 200 OK\nCSeq: ' + seq + '\nSession: ' + str(self.clientInfo['session'])
			connSocket = self.clientInfo['rtspSocket'][0]
			connSocket.send(reply.encode())
		
		# Error messages
		elif code == self.FILE_NOT_FOUND_404:
			print ("404 NOT FOUND")
		elif code == self.CON_ERR_500:
			print ("500 CONNECTION ERROR")
