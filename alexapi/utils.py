# Copyright (c) Gianmarco Garrisi 2017
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU General Public License as published by
#    the Free Software Foundation, either version 3 of the License, or
#    (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU General Public License for more details.
#
#    You should have received a copy of the GNU General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/>.

import picamera
import socket

class CameraManager:
	def __init__(self, soc):
		self.camera=picamera.PiCamera()
		self.sock=soc
		self.conn=None
	def take_picture(self):
                self.camera.resultion = (1024,768)
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
