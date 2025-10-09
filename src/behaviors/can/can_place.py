from behavior_tree import BTStatus, BTNode
from robot import EV3Robot


class CanPlace(BTNode):
    def __init__(self, robot: EV3Robot):
        self.robot = robot

    def tick(self) -> BTStatus:
        self.robot.gripper_motor.duty_cycle_sp = -50  # either 50 or -50 depending on motor orientation
        return BTStatus.SUCCESS
