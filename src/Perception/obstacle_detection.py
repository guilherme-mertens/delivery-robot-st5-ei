from arduino_interface import ArduinoInterface

class ObstacleDetection:
    """
    A class to detect obstacles using an Arduino interface.
    """

    def __init__(self, arduino_interface: ArduinoInterface):
        """
        Initialize the ObstacleDetection object with an Arduino interface.

        Args:
            arduino_interface (ArduinoInterface): The Arduino interface for obstacle detection.
        """
        self.arduino_interface = arduino_interface

    def get_detected_obstacle(self):
        """
        Detect if there is an obstacle.

        Returns:
            bool: True if an obstacle is detected, False otherwise.
        """
        distance = self.arduino_interface.get_detected_distance()
        if not distance:
            return False
        return 0 < distance < 6 and distance != 2
