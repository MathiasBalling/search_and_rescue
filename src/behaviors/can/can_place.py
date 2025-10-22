from behavior_tree import BTStatus, BTNode
from blackboard import BlackBoard
from robot import EV3Robot


class CanPlace(BTNode):
    def __init__(self, robot: EV3Robot, blackboard: BlackBoard):
        self.robot = robot
        self.blackboard = blackboard

    def tick(self) -> BTStatus:
        return BTStatus.SUCCESS
