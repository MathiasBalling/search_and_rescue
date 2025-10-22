import time
from behavior_tree import BTStatus, BTNode
from blackboard import BlackBoard
from robot import EV3Robot
from pid_controller import PIDController

from params import RETURN_TO_LINE_BASE_SPEED


class ReturnToLine(BTNode):
    def __init__(self, robot: EV3Robot, blackboard: BlackBoard):
        self.robot = robot
        self.blackboard = blackboard
        self.pid = PIDController(
            kp=1, ki=0.2, kd=0.1, setpoint=0, output_limits=(-100, 100)
        )

    def tick(self) -> BTStatus:
        return BTStatus.FAILURE
