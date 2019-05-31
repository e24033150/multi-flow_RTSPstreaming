import cv2

class VideoStream:
	def __init__(self, filename):
		self.filename = filename
		self.jpeg_quality = 70
		self.encode_param = [int(cv2.IMWRITE_JPEG_QUALITY), self.jpeg_quality]
		try:
			#self.file = open(filename, 'rb')
			self.file = cv2.VideoCapture(filename)
			self.fps = int(self.file.get(5))
			print (self.fps)
		except:
			raise IOError
		self.frameNum = 0
		
	def nextFrame(self):
		"""Get next frame."""
		#data = self.file.read(5) # Get the framelength from the first 5 bits
		ret, frame = self.file.read()
		if ret == True:
			#framelength = int(data)
							
			# Read the current frame
			#data = self.file.read(framelength)
			#strings = cv2.imencode('.jpg', frame, self.encode_param)[1]
			#cpy = strings.copy()
			self.frameNum += 1
		return cv2.imencode('.jpg', frame, self.encode_param)[1]
		#return frame
		
	def frameNbr(self):
		"""Get frame number."""
		return self.frameNum
	
	
