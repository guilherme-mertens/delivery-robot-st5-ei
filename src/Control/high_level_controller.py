from arduino_interface import ArduinoInterface
from Control.turning import Turning
from Control.pid_control import PID
from Control.stanley_controller import StanleyController

class HighLevelController:
    """
    High-level controller for robot actions.
    """

    def __init__(self, arduino_interface: ArduinoInterface):
        """
        Initialize the HighLevelController with an Arduino interface.

        Args:
            arduino_interface (ArduinoInterface): Interface to communicate with Arduino.
        """
        self.arduino_interface = arduino_interface
        self.action = 0
        self.turning_action = Turning(self.arduino_interface)
        self.pid_control = PID()
        self.stanley_controller = StanleyController()
        self.error = 0

    def set_action(self, set_action: int):
        """
        Set the current action to be performed by the controller.

        Args:
            set_action (int): Action to be set.
        """
        self.action = set_action

    def perform_action(self):
        """
        Perform the action based on the current action set.
        """
        if self.action == 0:
            w, v = self.pid_control.get_control_inputs(self.error)
            self.arduino_interface.set_wheel_velocity(w, v)
        elif self.action == 5:
            pass
        elif self.action == 4:
            self.turning_action.turn_180()
        elif self.action == 3:
            self.turning_action.turn_90_left()
        elif self.action == 2:
            self.turning_action.turn_90_right()
        elif self.action == 1:
            self.arduino_interface.stop()

    def update_error(self, point_to_be_followed):
        """
        Update the error for the controller.

        Args:
            point_to_be_followed (tuple): The point that the robot should follow.
        """
        self.error = self.stanley_controller.get_error(point_to_be_followed)
