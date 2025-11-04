import time

from ai.behaviors.behavior import Behavior
from actuators import ActuatorsProposal

from sensors.colors import ColorSensors
from sensors.gyro import GyroSensor

from utils.blackboard import BlackBoard
from utils.pid_controller import PIDController


from params import (
    LINE_FOLLOWING_BASE_SPEED,
    LINE_INTENSITY_THRESHOLD,
    LINE_FOLLOWING_PID_KP,
    LINE_FOLLOWING_PID_KD,
    LINE_FOLLOWING_PID_KI,
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
        self.pid = PIDController(
            LINE_FOLLOWING_PID_KP,
            LINE_FOLLOWING_PID_KI,
            LINE_FOLLOWING_PID_KD,
            (-100, 100),
        )
        self.limits = (-100, 100)
        self.base_speed = LINE_FOLLOWING_BASE_SPEED

    def update(self):
        l_val, r_val = self.color_sensors.get_value()
        now = time.time()
        if l_val < LINE_INTENSITY_THRESHOLD or r_val < LINE_INTENSITY_THRESHOLD:
            self.blackboard["last_time_line_seem"] = now

        if now - self.blackboard["last_time_line_seem"] > 2.0:
            self.weight = 0.0

        self.weight = 0.0

    def actuators_proposal(self):
        # TODO:
        return ActuatorsProposal(0, 0, False)

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
