class PID:
    """
    PID controller for controlling wheel velocities.
    """

    def __init__(self):
        """
        Initialize the PID controller with default parameters.
        """
        self.te = 2e-1
        self.kp = 0.15  # 0.2 for v=50
        self.ki = 0.000  # 0 for v=50
        self.kd = 0.00  # 0 for v=50
        self.i = 0
        self.e0 = 0

    def get_control_inputs(self, error: float):
        """
        Calculate the control inputs based on the current error.

        Args:
            error (float): The current error.

        Returns:
            tuple: The control inputs (u, v).
        """
        self.i += error * self.te
        d = (error - self.e0) / self.te
        u = self.kp * error + self.kd * d + self.ki * self.i
        self.e0 = error
        v = 50

        return u, v
