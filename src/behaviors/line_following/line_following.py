import time
from behavior_tree import BTStatus, BTNode
from blackboard import BlackBoard
from robot import EV3Robot
from pid_controller import PIDController

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


class LineFollowing(BTNode):
    def __init__(self, robot: EV3Robot, blackboard: BlackBoard):
        self.robot = robot
        self.blackboard = blackboard
        self.limits = (-100, 100)
        self.pid = PIDController(
            kp=LINE_FOLLOWING_PID_KP,
            ki=LINE_FOLLOWING_PID_KI,
            kd=LINE_FOLLOWING_PID_KD,
            setpoint=0,
            output_limits=self.limits,
        )
        self.controller_mode = 0

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
        self.pid.reset()

    def set_controller_uphill(self):
        if self.controller_mode == MODE_UPHILL:
            return
        self.pid.kp = 5
        self.pid.ki = 0
        self.pid.kd = 0
        self.controller_mode = MODE_UPHILL
        self.set_limits((-100, 100))
        self.pid.reset()

    def set_controller_downhill(self):
        if self.controller_mode == MODE_DOWNHILL:
            return
        self.pid.kp = 1
        self.pid.ki = 0
        self.pid.kd = 0
        self.controller_mode = MODE_DOWNHILL
        self.set_limits((-10, 10))
        self.pid.reset()

    def tick(self) -> BTStatus:
        current_time = time.time()

        if current_time - self.blackboard["last_time_line_seen"] > 2:
            # Not on line anymore
            return BTStatus.FAILURE

        left_color, right_color = self.robot.get_color_sensor_readings()

        if (
            left_color < LINE_INTENSITY_THRESHOLD
            and right_color < LINE_INTENSITY_THRESHOLD
        ):
            self.last_time_line_seen = current_time

        self.update_mode()

        diff = left_color - right_color

        control = self.pid.compute(diff, current_time)

        left_control = LINE_FOLLOWING_BASE_SPEED - control
        right_control = LINE_FOLLOWING_BASE_SPEED + control

        low_limit, up_limit = self.limits
        left_control = round(min(max(low_limit, left_control), up_limit))
        right_control = round(min(max(low_limit, right_control), up_limit))

        if left_color > 27:
            left_control = 100
            self.robot.set_wheel_duty_cycles(left=left_control, right=-50)
            # print("Sharp right turn ", left_color, right_color)

        elif right_color > 27:
            right_control = 100
            self.robot.set_wheel_duty_cycles(left=-50, right=right_control)
            print("Sharp left turn ", left_color, right_color)

        else:
            if abs((left_color - right_color)) <= 15:
                self.robot.set_wheel_duty_cycles(
                    left=LINE_FOLLOWING_BASE_SPEED, right=LINE_FOLLOWING_BASE_SPEED
                )
            else:
                self.robot.set_wheel_duty_cycles(left=left_control, right=right_control)
            print(
                # "PID control",
                # control,
                # left_control,
                # right_control,
                # "Colors:",
                # left_color,
                # right_color,
            )

        return BTStatus.RUNNING

    def update_mode(self):
        rate = self.robot.gyro_sensor.value()
        if rate > 25:
            if self.controller_mode == MODE_STRAIGHT:
                self.set_controller_uphill()
            else:
                self.set_controller_straight()
        elif rate < -25:
            if self.controller_mode == MODE_STRAIGHT:
                self.set_controller_downhill()
            else:
                self.set_controller_straight()
        print("Angle:", rate, "Mode:", self.controller_mode)
