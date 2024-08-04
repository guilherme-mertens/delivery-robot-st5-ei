from math import atan

class StanleyController:
    """
    Stanley controller for calculating the control error.
    """

    def __init__(self):
        """
        Initialize the StanleyController with default parameters.
        """
        self.k_cross_track_error = 1

    def get_error(self, point_to_be_followed: tuple):
        """
        Calculate the error based on the point to be followed.

        Args:
            point_to_be_followed (tuple): The point that the robot should follow.

        Returns:
            float: The calculated error.
        """
        return self.k_cross_track_error * point_to_be_followed[0]  # + atan(x/y)