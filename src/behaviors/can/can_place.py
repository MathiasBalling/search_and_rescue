from typing import override
from behavior_tree import BTStatus, BTNode


class CanPlace(BTNode):
    def __init__(self, robot):
        self.robot = robot

    @override
    def tick(self) -> BTStatus:
        # TODO: Make placing object behavior
        return BTStatus.SUCCESS
