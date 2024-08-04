import cv2
from picamera.array import PiRGBArray
import picamera

class Camera:
    """
    A class to interface with the Raspberry Pi Camera.
    """

    def __init__(self):
        """
        Initialize the Camera object with specific resolution and framerate.
        """
        self.camera = picamera.PiCamera()
        self.camera.resolution = (480, 272)
        self.camera.framerate = 80
        self.camera.start_recording('testRecording.h264')
        self.cap = PiRGBArray(self.camera, size=(480, 272))

    def get_image(self):
        """
        Capture an image from the camera.

        Returns:
            numpy.ndarray: The captured image in BGR format.
        """
        self.camera.capture(self.cap, use_video_port=True, resize=(480, 272), format="bgr")
        img = self.cap.array
        self.cap.truncate(0)
        return img
