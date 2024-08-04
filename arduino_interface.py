from robust_serial import write_order, Order, write_i8, write_i16, read_i16, read_i32, read_i8
from robust_serial.utils import open_serial_port
from constants import BAUDRATE
import time
import struct
import func_timeout


class ArduinoInterface():

    def __init__(self):
        self.serial_file = None
        self.connect_to_arduino()

    def set_wheel_velocity(self, angular_velocity, velocity):
        write_order(self.serial_file, Order.MOTOR)
        left_speed = velocity + angular_velocity
        right_speed = velocity - angular_velocity
        if right_speed > 100:
            right_speed = 100
        if right_speed < 10:
            if right_speed == -100 or right_speed == 0:
                pass
            else:
                right_speed = 10
        if left_speed > 100:
            left_speed = 100
        if left_speed < 10:
            if left_speed == -100 or left_speed == 0:
                pass
            else:
                left_speed = 10
        write_i8(self.serial_file, int(right_speed))
        write_i8(self.serial_file, int(left_speed))
        self.serial_file.reset_input_buffer()
        self.serial_file.reset_output_buffer()

    def set_wheel_left(self):
        write_order(self.serial_file, Order.MOTOR)
        write_i8(self.serial_file, 0)
        write_i8(self.serial_file, 100)
        self.serial_file.reset_input_buffer()
        self.serial_file.reset_output_buffer()

    def set_wheel_right(self):
        write_order(self.serial_file, Order.MOTOR)
        write_i8(self.serial_file, 100)
        write_i8(self.serial_file, 0)
        self.serial_file.reset_input_buffer()
        self.serial_file.reset_output_buffer()

    def stop(self):
        write_order(self.serial_file, Order.MOTOR)
        write_i8(self.serial_file, 0)
        write_i8(self.serial_file, 0)
        # write_order(self.serial_file, Order.STOP_ORDER)

    def get_dected_distance(self):
        self.serial_file.reset_input_buffer()
        self.serial_file.reset_output_buffer()
        time.sleep(0.01)
        try:
            d = self.distance_aux()
        except:
            return 40
        self.serial_file.reset_input_buffer()
        self.serial_file.reset_output_buffer()
        print("Obstacles: ", d)
        return d
    
    def distance_aux(self):
        write_order(self.serial_file, Order.ULTRASONIC)
        d = read_i16(self.serial_file)
        return d


    def connect_to_arduino(self):
        try:
            # Open serial port (for communication with Arduino)
            self.serial_file = open_serial_port(baudrate=BAUDRATE)
        except Exception as e:
            print('exception')
            raise e

        is_connected = False
        # Initialize communication with Arduino
        while not is_connected:
            print("Trying connection to Arduino...")
            write_order(self.serial_file, Order.HELLO)
            bytes_array = bytearray(self.serial_file.read(1))
            if not bytes_array:
                time.sleep(2)
                continue
            byte = bytes_array[0]
            if byte in [Order.HELLO.value, Order.ALREADY_CONNECTED.value]:
                is_connected = True

        time.sleep(2)
        c = 1
        while (c != b''):
            c = self.serial_file.read(1)
