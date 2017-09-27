import picamera

class CameraManager:
	def __init__(self):
		self.camera=picamera.PiCamera()
		self.socket=None
		self.conn=None
	def take_picture(self):
		self.camera.capture('tmp.jpg')
	def start_video_stream(socket):
		self.socket = socket
		self.conn = socket.accept()[0].makefile('f')
		self.camera.start_recording(conn, format='h264')
	def stop_video_stream():
		try:
			self.camera.stop_recording()
		finally:
			self.conn.close()
			self.conn = None
			self.socket.close()
			self.socket = None
