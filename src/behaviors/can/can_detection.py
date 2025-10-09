from behavior_tree import BTStatus, BTNode
from robot import EV3Robot


class CanDetection(BTNode):
    def __init__(self, robot: EV3Robot):
        self.robot = robot
        self.ultrasound = robot.ultrasound_sensor
        self.right_motor = robot.right_motor
        self.left_motor = robot.left_motor
        self.can_found = False

    def detecting_can(self) -> bool:
        distance = self.ultrasound.value() / 10
        self.right_motor.duty_cycle_sp = 10
        self.left_motor.duty_cycle_sp = -10
        print("Distance to can:", distance, "cm")
        if distance < 10:
            self.right_motor.duty_cycle_sp = 0
            self.left_motor.duty_cycle_sp = 0
            self.can_found = True
            return self.can_found

    def tick(self) -> BTStatus:
        if self.detecting_can():
            return BTStatus.SUCCESS
        return BTStatus.FAILURE
