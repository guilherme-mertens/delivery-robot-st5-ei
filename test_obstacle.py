from Perception.camera import Camera
from Perception.line_detection import LineDetection
from Control.stanley_controller import StanleyController
from Control.pid_control import PID
from arduino_interface import ArduinoInterface
from Decission.state_machine import StateMachine
from Control.high_level_controller import HighLevelController
from Decission.mission_planner import MisionPlanner
from Perception.corner_detection import CornerDetection
from Perception.obstacle_detection import ObstacleDetection
from multiprocessing import Queue, Process, Manager
import time


arduino_interface = ArduinoInterface()
obstacle_detector = ObstacleDetection(arduino_interface)
high_level_controller = HighLevelController(arduino_interface)

while True:
    obstacles = obstacle_detector.get_detected_obstacle()
    # time.sleep(0.5)
    print(obstacles)
    if obstacles:
        high_level_controller.set_action(4)
        high_level_controller.perform_action()
