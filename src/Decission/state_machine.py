class StateMachine:
    """
    State machine for managing robot states.
    """

    def __init__(self):
        """
        Initialize the StateMachine with default state.
        
        States:
        0 -> WAITING MISSION PLANNER
        1 -> FOLLOWING LINE
        2 -> AVOIDING OBSTACLE
        3 -> PERFORMING MISSION ACTION
        4 -> LOSS MODE
        """
        self.STATE = 0

    def return_state(self) -> int:
        """
        Return the current state of the state machine.

        Returns:
            int: The current state.
        """
        return self.STATE

    def decide_state(self, corner: bool, obstacle: bool):
        """
        Decide the state based on the presence of a corner or obstacle.

        Args:
            corner (bool): True if there is a corner.
            obstacle (bool): True if there is an obstacle.
        """
        if obstacle:
            self.STATE = 2
        elif corner:
            self.STATE = 0
