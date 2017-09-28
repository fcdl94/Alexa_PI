import picamera
import socket

class CameraManager:
	def __init__(self, socket):
		self.camera=picamera.PiCamera()
		self.socket=socket
		self.conn=None
	def take_picture(self):
		self.camera.capture('tmp.jpg')
	def start_video_stream():
                self.camera.resolution(640, 480)
                self.camera.framerate(24)
		self.conn = self.socket.makefile('f')
		self.camera.start_recording(conn, format='h264')
	def stop_video_stream():
		try:
			self.camera.stop_recording()
		finally:
			self.conn.close()
			self.conn = None
