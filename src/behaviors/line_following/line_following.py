from typing import override
from behavior_tree import BTStatus, BTNode
from robot import EV3Robot


class LineFollowing(BTNode):
    def __init__(self, robot: EV3Robot):
        self.robot = robot

    @override
    def tick(self) -> BTStatus:
        # TODO: Make line following behavior
        print("Sensor readings", self.robot.get_color_sensor_readings())
        self.robot.left_motor.duty_cycle_sp = 100
        self.robot.right_motor.duty_cycle_sp = 50

        return BTStatus.RUNNING
