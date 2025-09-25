import time
from typing import override
from behavior_tree import BTStatus, BTNode
from robot import EV3Robot
from pid_controller import PIDController

BASE_SPEED = 50


class LineFollowing(BTNode):
    def __init__(self, robot: EV3Robot):
        self.robot = robot
        self.pid = PIDController(
            kp=1, ki=0.1, kd=0, setpoint=0, output_limits=(-100, 100)
        )
        self._last_time_line_seen = time.time()

    @override
    def tick(self) -> BTStatus:
        left_color, right_color = self.robot.get_color_sensor_readings()
        current_time = time.time()

        print(
            "Sensor readings",
            left_color,
            right_color,
        )

        control = self.pid.compute(left_color - right_color, current_time)

        left_control = BASE_SPEED - control
        right_control = BASE_SPEED + control

        left_control = min(max(0, left_control), 100)
        right_control = min(max(0, right_control), 100)

        self.robot.left_motor.duty_cycle_sp = left_control
        self.robot.right_motor.duty_cycle_sp = right_control

        return BTStatus.RUNNING
