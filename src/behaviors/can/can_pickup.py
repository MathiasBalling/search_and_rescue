from behavior_tree import BTStatus, BTNode
from robot import EV3Robot


class CanPickup(BTNode):
    def __init__(self, robot: EV3Robot):
        self.robot = robot
        self.object_picked_up = False
        self.gripper = robot.gripper_motor

    def tick(self) -> BTStatus:
        if not self.object_picked_up:
            self.gripper.duty_cycle_sp = 0
            if self.robot.touch_sensor.value() == 1:
                self.gripper.duty_cycle_sp = 50  # either 50 or -50 depending on motor orientation
                self.object_picked_up = True
        return BTStatus.SUCCESS
