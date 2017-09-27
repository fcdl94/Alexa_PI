import picamera

class CameraManager:
    def __init__(self):
        self.camera=picamera.PiCamera()
    def take_picture(self):
        self.camera.capture('tmp.jpg')
    
