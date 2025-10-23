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


class LineFollowing(BTNode):
    def __init__(self, robot: EV3Robot, blackboard: BlackBoard):
        self.robot = robot
        self.blackboard = blackboard
        # self.ultra_sound_sensor = robot.ultrasound_sensor
        self.pid = PIDController(
            kp=LINE_FOLLOWING_PID_KP,
            ki=LINE_FOLLOWING_PID_KI,
            kd=LINE_FOLLOWING_PID_KD,
            setpoint=0,
            output_limits=(-100, 100),
        )

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

        self.robot.set_wheel_duty_cycles(left=0, right=0)

        diff = left_color - right_color

        control = self.pid.compute(diff, current_time)

        # print("Time:", current_time, "Diff:", diff, "Control:", control)

        left_control = LINE_FOLLOWING_BASE_SPEED - control
        right_control = LINE_FOLLOWING_BASE_SPEED + control

        left_control = round(min(max(0, left_control), 100))
        right_control = round(min(max(0, right_control), 100))

        if False and abs(control) <= 80:
            self.robot.set_wheel_duty_cycles(
                left=LINE_FOLLOWING_BASE_SPEED, right=LINE_FOLLOWING_BASE_SPEED
            )
            print(
                "Going straight",
                control,
                left_control,
                right_control,
                "Colors:",
                left_color,
                right_color,
            )

        elif left_color > 40:
            left_control = 100
            self.robot.set_wheel_duty_cycles(left=left_control, right=-50)
            print("Sharp right turn")

        elif right_color > 40:
            right_control = 100
            self.robot.set_wheel_duty_cycles(left=-50, right=right_control)
            print("Sharp left turn")

        else:
            self.robot.set_wheel_duty_cycles(left=left_control, right=right_control)
            print(
                "PID control",
                control,
                left_control,
                right_control,
                "Colors:",
                left_color,
                right_color,
            )

        return BTStatus.RUNNING
