from behavior_tree import BTStatus, BTNode, BlackBoard
from time import sleep
from robot import EV3Robot


class CanPickup(BTNode):
    def __init__(self, robot: EV3Robot, blackboard: BlackBoard):
        self.robot = robot
        self.blackboard = blackboard
        self.object_picked_up = False

    def tick(self) -> BTStatus:
        if not self.object_picked_up:
            self.robot.gripper_motor.duty_cycle_sp = 0
            distance = self.robot.ultrasound_sensor.value() / 10
            print("Distance to can:", distance, "cm")
            self.robot.right_motor.duty_cycle_sp = -40
            self.robot.left_motor.duty_cycle_sp = -40
            if distance < 5:
                self.robot.right_motor.duty_cycle_sp = 0
                self.robot.left_motor.duty_cycle_sp = 0
                sleep(1)
                self.robot.gripper_motor.duty_cycle_sp = 50
                sleep(3)
                self.robot.gripper_motor.duty_cycle_sp = 0
                self.object_picked_up = True
        return BTStatus.SUCCESS
