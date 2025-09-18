from typing import override
from behavior_tree import BTStatus, BTNode


class CanDetection(BTNode):
    def __init__(self, robot):
        self.robot = robot

    @override
    def tick(self) -> BTStatus:
        # TODO: Make object detection behavior
        return BTStatus.FAILURE
