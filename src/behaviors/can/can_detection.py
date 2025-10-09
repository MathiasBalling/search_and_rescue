from behavior_tree import BTStatus, BTNode
from robot import EV3Robot


class CanDetection(BTNode):
    def __init__(self, robot: EV3Robot):
        self.robot = robot
        self.ultrasound = robot.ultrasound_sensor

    def tick(self) -> BTStatus:
        distance = self.ultrasound.value() / 10
        if distance < 20:
            print(f"Can detected at distance: {distance} cm")
            return BTStatus.SUCCESS
        return BTStatus.FAILURE
