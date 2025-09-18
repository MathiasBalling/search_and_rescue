from typing import override
from behavior_tree import BTStatus, BTNode


class CanPickup(BTNode):
    def __init__(self, robot):
        self.robot = robot
        self.object_picked_up = False

    @override
    def tick(self) -> BTStatus:
        if not self.object_picked_up:
            # TODO: Make gripping behavior
            return BTStatus.FAILURE
        return BTStatus.SUCCESS
