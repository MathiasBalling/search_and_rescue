import time
from behavior_tree import BTStatus, BTNode
from robot import EV3Robot
from pid_controller import PIDController

BASE_SPEED = 70


class ReturnToLine(BTNode):
    def __init__(self, robot: EV3Robot):
        self.robot = robot
        self.pid = PIDController(
            kp=1, ki=0.2, kd=0.1, setpoint=0, output_limits=(-100, 100)
        )

    def tick(self) -> BTStatus:
        return BTStatus.FAILURE
