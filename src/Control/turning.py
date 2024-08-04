from arduino_interface import ArduinoInterface
import time

class Turning:
    """
    Class for performing turning actions using an Arduino interface.
    """

    def __init__(self, arduino_interface: ArduinoInterface):
        """
        Initialize the Turning object with an Arduino interface.

        Args:
            arduino_interface (ArduinoInterface): Interface to communicate with Arduino.
        """
        self.arduino_interface = arduino_interface

    def turn_90_left(self):
        """
        Turn the robot 90 degrees to the left.
        """
        time.sleep(0.2)
        self.arduino_interface.set_wheel_right()
        time.sleep(1.85)
        self.arduino_interface.set_wheel_velocity(0, 0)

    def turn_90_right(self):
        """
        Turn the robot 90 degrees to the right.
        """
        time.sleep(0.2)
        self.arduino_interface.set_wheel_left()
        time.sleep(1.85)
        self.arduino_interface.set_wheel_velocity(0, 0)

    def turn_180(self):
        """
        Turn the robot 180 degrees.
        """
        self.arduino_interface.set_wheel_velocity(100, 0)
        time.sleep(1.85)
        self.arduino_interface.set_wheel_velocity(0, 0)
