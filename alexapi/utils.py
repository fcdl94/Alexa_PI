import picamera
import socket

class CameraManager:
	def __init__(self, soc):
		self.camera=picamera.PiCamera()
		self.sock=soc
		self.conn=None
	def take_picture(self):
		self.camera.capture('tmp.jpg')
	def start_video_stream(self):
                self.camera.resolution = (640, 480)
                self.camera.framerate = 24
		self.conn = self.sock.makefile(mode='wb')
		self.camera.start_recording(self.conn, format='h264')
	def stop_video_stream(self):
		try:
			self.camera.stop_recording()
		finally:
			self.conn.close()
			self.conn = None
