from typing import override
from behavior_tree import BTStatus, BTNode


class LineFollowing(BTNode):
    def __init__(self, robot):
        self.robot = robot

    @override
    def tick(self) -> BTStatus:
        # TODO: Make line following behavior
        return BTStatus.RUNNING
