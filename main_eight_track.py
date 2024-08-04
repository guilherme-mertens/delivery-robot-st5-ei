from Perception.camera import Camera
from Perception.computer_vision import ComputerVision
from Control.stanley_controller import StanleyController
from Control.pid_control import PID
from arduino_interface import ArduinoInterface
import time

if __name__=="__main__":

    camera = Camera()
    computer_vision = ComputerVision()
    stanley_controller = StanleyController()
    pid = PID()
    velocity = 50
    arduino_interface = ArduinoInterface()
    while True:
        try:
            image = camera.get_image()
            x, y = computer_vision.get_edges(image)
            error = stanley_controller.get_error(x, y)
            angular_velocity = pid.get_angular_velocity(error)
            arduino_interface.set_wheel_velocity(angular_velocity, velocity)
            time.sleep(0.01)
        except:
            arduino_interface.stop()
            break



