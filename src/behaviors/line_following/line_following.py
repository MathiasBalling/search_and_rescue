import time
from behavior_tree import BTStatus, BTNode, BlackBoard
from robot import EV3Robot
from pid_controller import PIDController

from params import (
    LINE_FOLLOWING_BASE_SPEED,
    LINE_FOLLOWING_COLOR_THRESHOLD,
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
        self._last_time_line_seen = time.time()

    def tick(self) -> BTStatus:
        left_color, right_color = self.robot.get_color_sensor_readings()
        current_time = time.time()


        self.robot.left_motor.duty_cycle_sp = 0
        self.robot.right_motor.duty_cycle_sp = 0

        diff = left_color - right_color

        control = self.pid.compute(diff, current_time)

        left_control = LINE_FOLLOWING_BASE_SPEED - control
        right_control = LINE_FOLLOWING_BASE_SPEED + control

        left_control = round(min(max(0, left_control), 100))
        right_control = round(min(max(0, right_control), 100))

        if abs(diff) <= 30:
            left_control = LINE_FOLLOWING_BASE_SPEED
            right_control = LINE_FOLLOWING_BASE_SPEED
            print("On track")
        
        elif left_color > 40:
            left_control = 100
            self.robot.left_motor.duty_cycle_sp = left_control
            self.robot.right_motor.duty_cycle_sp = -50
            print("Sharp right turn")

        elif right_color > 40:
            right_control = 100
            self.robot.right_motor.duty_cycle_sp = right_control
            self.robot.left_motor.duty_cycle_sp = -50
            print("Sharp left turn")


        self.robot.left_motor.duty_cycle_sp = left_control
        self.robot.right_motor.duty_cycle_sp = right_control

        print(
            "Sensor readings",
            left_color,
            right_color,
            # self.ultra_sound_sensor.value() / 10,
            control,
            left_control,
            right_control,
            diff,
        )

        return BTStatus.RUNNING
