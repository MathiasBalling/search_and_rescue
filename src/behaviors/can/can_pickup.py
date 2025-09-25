from behavior_tree import BTStatus, BTNode
from robot import EV3Robot


class CanPickup(BTNode):
    def __init__(self, robot: EV3Robot):
        self.robot = robot
        self.object_picked_up = False

    def tick(self) -> BTStatus:
        if not self.object_picked_up:
            # TODO: Make gripping behavior
            return BTStatus.FAILURE
        return BTStatus.SUCCESS
