from typing import override
from behavior_tree import BTStatus, BTNode
from robot import EV3Robot


class CanDetection(BTNode):
    def __init__(self, robot: EV3Robot):
        self.robot = robot

    @override
    def tick(self) -> BTStatus:
        # TODO: Make object detection behavior
        return BTStatus.FAILURE
