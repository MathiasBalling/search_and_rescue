from behavior_tree import BTStatus, BTNode, BlackBoard
from robot import EV3Robot


class CanPlace(BTNode):
    def __init__(self, robot: EV3Robot, blackboard: BlackBoard):
        self.robot = robot
        self.blackboard = blackboard
        self.gripper = robot.gripper_motor

    def tick(self) -> BTStatus:
        self.gripper.duty_cycle_sp = -50
        return BTStatus.SUCCESS
