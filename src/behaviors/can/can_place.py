from behavior_tree import BTStatus, BTNode
from robot import EV3Robot


class CanPlace(BTNode):
    def __init__(self, robot: EV3Robot):
        self.robot = robot

    def tick(self) -> BTStatus:
        # TODO: Make placing object behavior
        return BTStatus.SUCCESS
