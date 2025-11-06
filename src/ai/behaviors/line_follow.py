import time

from ai.behaviors.behavior import Behavior
from actuators import ActuatorsProposal, WheelCommand

from sensors.colors import ColorSensors
from sensors.gyro import GyroSensor

from utils.blackboard import BlackBoard
from utils.pid_controller import PIDController


from params import (
    LINE_FOLLOWING_BASE_SPEED,
    LINE_INTENSITY_WHITE_THRESHOLD,
    LINE_INTENSITY_BLACK_THRESHOLD,
    LINE_FOLLOWING_PID_KP,
    LINE_FOLLOWING_PID_KD,
    LINE_FOLLOWING_PID_KI,
    LINE_FOLLOWING_SHARP_TURN_SPEED,
)

MODE_STRAIGHT = 0
MODE_UPHILL = 1
MODE_DOWNHILL = 2


class LineFollowingBehavior(Behavior):
    # Required methods
    def __init__(
        self, blackboard: BlackBoard, color_sensors: ColorSensors, gyro: GyroSensor
    ):
        super().__init__(blackboard, 1.0)  # 1.0 because we start on the line
        self.color_sensors = color_sensors
        self.gyro = gyro
        self.limits = (-100, 100)
        self.pid = PIDController(
            LINE_FOLLOWING_PID_KP,
            LINE_FOLLOWING_PID_KI,
            LINE_FOLLOWING_PID_KD,
            self.limits,
        )
        self.controller_mode = MODE_STRAIGHT
        self.limits = (-100, 100)
        self.base_speed = LINE_FOLLOWING_BASE_SPEED
        self.last_sensor_seen = "left"

    def update(self):
        l_val, r_val = self.color_sensors.get_value()
        now = time.time()
        if (
            l_val < LINE_INTENSITY_WHITE_THRESHOLD
            or r_val < LINE_INTENSITY_WHITE_THRESHOLD
        ):
            self.blackboard["last_time_line_seen"] = now

        if now - self.blackboard["last_time_line_seen"] > 2.0:
            self.weight = 0.0

        self.weight = 0.0

    def actuators_proposal(self):
        cmd = self.follow_line()
        return ActuatorsProposal(cmd)

    # Other methods
    def set_limits(self, limit):
        self.limits = limit
        self.pid.output_limits = limit

    def set_controller_straight(self):
        if self.controller_mode == MODE_STRAIGHT:
            return
        self.pid.kp = LINE_FOLLOWING_PID_KP
        self.pid.ki = LINE_FOLLOWING_PID_KI
        self.pid.kd = LINE_FOLLOWING_PID_KD
        self.controller_mode = MODE_STRAIGHT
        self.set_limits((0, 100))
        self.base_speed = LINE_FOLLOWING_BASE_SPEED
        self.pid.reset()

    def set_controller_uphill(self):
        if self.controller_mode == MODE_UPHILL:
            return
        # TODO: Update these
        self.pid.kp = 5
        self.pid.ki = 0
        self.pid.kd = 0
        self.controller_mode = MODE_UPHILL
        self.set_limits((-100, 100))
        self.base_speed = 100
        self.pid.reset()

    def set_controller_downhill(self):
        if self.controller_mode == MODE_DOWNHILL:
            return
        # TODO: Update these
        self.pid.kp = 1
        self.pid.ki = 0
        self.pid.kd = 0
        self.controller_mode = MODE_DOWNHILL
        self.set_limits((-10, 10))
        self.base_speed = 100
        self.pid.reset()

    def update_mode(self):
        # FIX: Shifts to fast to new state
        rate = self.gyro.get_value()
        if rate > 25:
            if self.controller_mode == MODE_STRAIGHT:
                self.set_controller_uphill()
            elif self.controller_mode == MODE_DOWNHILL:
                self.set_controller_straight()
        elif rate < -25:
            if self.controller_mode == MODE_STRAIGHT:
                self.set_controller_downhill()
            elif self.controller_mode == MODE_UPHILL:
                self.set_controller_straight()
        print("Angle:", rate, "Mode:", self.controller_mode)

    def follow_line(self):
        current_time = time.time()

        left_color, right_color = self.color_sensors.get_value()

        # self.update_mode()

        diff = left_color - right_color

        control = self.pid.compute(diff, current_time)

        left_control = self.base_speed - control
        right_control = self.base_speed + control

        left_control = round(min(max(self.limits[0], left_control), self.limits[1]))
        right_control = round(min(max(self.limits[0], right_control), self.limits[1]))
        print(
            # "PID control",
            # control,
            # left_control,
            # right_control,
            "Colors:",
            left_color,
            right_color,
        )

        if (
            left_color <= LINE_INTENSITY_BLACK_THRESHOLD
            and right_color >= LINE_INTENSITY_WHITE_THRESHOLD
        ):  # TURN LEFT SHARP
            self.last_sensor_seen = "left"
            return WheelCommand(
                left_speed=-LINE_FOLLOWING_SHARP_TURN_SPEED + 20,
                right_speed=LINE_FOLLOWING_SHARP_TURN_SPEED,
            )
        elif (
            right_color <= LINE_INTENSITY_BLACK_THRESHOLD
            and left_color >= LINE_INTENSITY_WHITE_THRESHOLD
        ):  # TURN RIGHT SHARP
            self.last_sensor_seen = "right"
            return WheelCommand(
                left_speed=LINE_FOLLOWING_SHARP_TURN_SPEED,
                right_speed=-LINE_FOLLOWING_SHARP_TURN_SPEED + 20,
            )
        elif (
            left_color <= LINE_INTENSITY_BLACK_THRESHOLD
            and right_color <= LINE_INTENSITY_BLACK_THRESHOLD
        ):  # SE BOTH BLACK
            if self.last_sensor_seen == "left":
                return WheelCommand(
                    left_speed=-LINE_FOLLOWING_SHARP_TURN_SPEED + 20,
                    right_speed=LINE_FOLLOWING_SHARP_TURN_SPEED,
                )
            else:
                return WheelCommand(
                    left_speed=LINE_FOLLOWING_SHARP_TURN_SPEED,
                    right_speed=-LINE_FOLLOWING_SHARP_TURN_SPEED + 20,
                )

        return WheelCommand(left_speed=left_control, right_speed=right_control)
