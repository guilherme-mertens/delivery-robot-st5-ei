
from Perception.camera import Camera
from Perception.line_detection import LineDetection
from Control.stanley_controller import StanleyController
from Control.pid_control import PID
from arduino_interface import ArduinoInterface
from Decission.state_machine import StateMachine
from Control.high_level_controller import HighLevelController
from Decission.mission_planner import Graph
from Perception.corner_detection import CornerDetection
from Perception.obstacle_detection import ObstacleDetection
import time
from multiprocessing import Queue, Process, Manager

def run_obstacle_detection(detected_obstacle_queue, obstacle_queue):
    while True:
        a = detected_obstacle_queue.get()
        obstacles = obstacle_detector.get_detected_obstacle()
        obstacle_queue.put(obstacles)
        # time.sleep(0.01)




#def run_obstacle_detection(obstacle_buffer):
#    while True:
#        obstacles = obstacle_detector.get_detected_obstacle()
#        obstacle_buffer.value = obstacles
#        time.sleep(0.5)



def run_line_detection(line_image_queue, line_queue):
    # line_detector = LineDetection()
    while True:
        t0 = time.time()
        line = line_detector.get_line_detected(line_image_queue.get())
        # print(time.time() - t0)
        line_queue.put(line)
        # time.sleep(0.01)



if __name__=="__main__":
    arduino_interface = ArduinoInterface()
    camera = Camera()
    line_detector = LineDetection()
    corner_detector = CornerDetection()
    obstacle_detector = ObstacleDetection(arduino_interface)


    state_machine = StateMachine()
    high_level_controller = HighLevelController(arduino_interface)
    mission_planner = Graph(5, 5, "A", "C")
    # mission_planner.get_trajectory()
    next_action = 0
    # detected_obstacle_queue = Queue()
    # obstacle_queue = Queue()
    # obstacle_process = Process(target=run_obstacle_detection, args=[detected_obstacle_queue, obstacle_queue])
    # obstacle_process.start()

    # manager = Manager()
    # x = manager.Value('i', 0)
    # obstacle_process = Process(target=run_obstacle_detection, args=[x])
    # obstacle_process.start()

    line_image_queue = Queue()
    line_queue = Queue()
    line_process = Process(target=run_line_detection, args=(line_image_queue, line_queue))
    line_process.start()
    n = 0
    obstacles = False

    while True:
        if state_machine.return_state() == 0:
            # next_action = mission_planner.get_next_action()
            next_action = 0
            state_machine.STATE = 3

        elif state_machine.return_state() == 1:
            n += 1
            # t0 = time.time()
            # detected_obstacle_queue.put(0)
            # obstacles = obstacle_detector.get_detected_obstacle()
            image = camera.get_image()
            # print(time.time()-t0)
            # t0 = time.time()
            
            line_image_queue.put(image)
            # obstacles = obstacle_detector.get_detected_obstacle()
            if n == 3:
                obstacles = obstacle_detector.get_detected_obstacle()
                n = 0
            point_to_be_followed = line_queue.get()
            # obstacles = x.value
            # print(time.time()-t0)
            # t0 = time.time()
            # detected_obstacle_queue.put(0)
            # obstacles = obstacle_queue.get()
            # time.sleep(0.01)
            # obstacles = obstacle_detector.get_detected_obstacle()
            # time.sleep(0.01)
            # print(point_to_be_followed)
            # print(time.time()-t0)
            
            # print(point_to_be_followed)
            corners = False
            # obstacles = obstacle_detector.get_detected_obstacle()
            # obstacles = False
            high_level_controller.update_error(point_to_be_followed)
            high_level_controller.perform_action()
            # obstacles = obstacle_queue.get()
            # obstacles = False
            state_machine.decide_state(corners, obstacles)
            # print(time.time()-t0)


        elif state_machine.return_state() == 2:
            print("a")
            obstacles = False
            high_level_controller.set_action(4)
            high_level_controller.perform_action()
            # mission_planner.recompute()
            state_machine.STATE = 1
            high_level_controller.set_action(0)


        elif state_machine.return_state() == 3:
            high_level_controller.set_action(next_action)
            high_level_controller.perform_action()
            state_machine.STATE = 1
            high_level_controller.set_action(0)






