import ev3dev.ev3 as ev3
from ev3dev2.sound import Sound
import time
import math

from params import MOTOR_OFF


class EV3Robot:
    def __init__(self):
        self.filtered_left_color = 0
        self.filtered_right_color = 0
        self.filter_alpha_color = 0.50  # Adjust for smoothing

        # Set up motors
        self.left_motor = ev3.LargeMotor(ev3.OUTPUT_A)
        self.right_motor = ev3.LargeMotor(ev3.OUTPUT_D)
        self.gripper_motor = ev3.MediumMotor(ev3.OUTPUT_C)
        self.left_motor.run_direct()
        self.right_motor.run_direct()
        self.gripper_motor.run_direct()
        self.gripper_closed = False

        assert self.left_motor.connected, "Left motor is not connected to port A"
        assert self.right_motor.connected, "Right motor is not connected to port B"
        assert self.gripper_motor.connected, "Gripper motor is not connected to port C"

        # Set up sensors
        self.left_color_sensor = ev3.ColorSensor(ev3.INPUT_1)
        self.right_color_sensor = ev3.ColorSensor(ev3.INPUT_4)
        self.left_color_sensor.mode = ev3.ColorSensor.MODE_COL_REFLECT
        self.right_color_sensor.mode = ev3.ColorSensor.MODE_COL_REFLECT
        self.ultrasound_sensor = ev3.UltrasonicSensor(ev3.INPUT_2)
        self.ultrasound_sensor.mode = "US-DIST-CM"

        assert self.right_color_sensor.connected, (
            "Right color sensor 1 is not connected to port 4"
        )
        assert self.left_color_sensor.connected, (
            "Left color sensor 2 is not connected to port 1"
        )
        assert self.ultrasound_sensor.connected, (
            "Ultrasound sensor is not connected to port 2"
        )

        # Set up sound
        self.speaker = Sound()
        self.speaker.speak("bing bong")

    def get_color_sensor_readings(self):
        left = self.left_color_sensor.value()
        right = self.right_color_sensor.value()
        self.filtered_left_color = (
            self.filter_alpha_color * left
            + (1 - self.filter_alpha_color) * self.filtered_left_color
        )
        self.filtered_right_color = (
            self.filter_alpha_color * right
            + (1 - self.filter_alpha_color) * self.filtered_right_color
        )
        return (self.filtered_left_color, self.filtered_right_color)

    def get_ultrasound_sensor_reading(self):
        return self.ultrasound_sensor.value() / 10.0

    def set_wheel_duty_cycles(self, left, right):
        self.left_motor.duty_cycle_sp = left
        self.right_motor.duty_cycle_sp = right

    def open_gripper(self):
        if self.gripper_closed:
            self.gripper_motor.duty_cycle_sp = 40
            time.sleep(3)
            self.gripper_motor.duty_cycle_sp = 0
            self.gripper_closed = False

    def close_gripper(self):
        if not self.gripper_closed:
            self.gripper_motor.duty_cycle_sp = -40
            time.sleep(3)
            self.gripper_motor.duty_cycle_sp = 0
            self.gripper_closed = True

    def can_pickup(self) -> bool:
        distance = self.get_ultrasound_sensor_reading()
        print("Distance to can pickup:", distance, "cm")
        if distance < 5:
            self.set_wheel_duty_cycles(left=15, right=15)
            self.close_gripper()
            print("Can picked up!")
            time.sleep(2)
            self.set_wheel_duty_cycles(left=MOTOR_OFF, right=MOTOR_OFF)
            return True
        return False
