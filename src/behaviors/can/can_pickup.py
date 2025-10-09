from behavior_tree import BTStatus, BTNode
from time import sleep
from robot import EV3Robot


class CanPickup(BTNode):
    def __init__(self, robot: EV3Robot):
        self.robot = robot
        self.object_picked_up = False
        self.gripper = robot.gripper_motor
        self.ultrasonic = robot.ultrasound_sensor
        self.right_motor = robot.right_motor
        self.left_motor = robot.left_motor

    def tick(self) -> BTStatus:
        if not self.object_picked_up:
            self.gripper.duty_cycle_sp = 0
            distance = self.ultrasonic.value() / 10
            print("Distance to can:", distance, "cm")
            self.right_motor.duty_cycle_sp = -40
            self.left_motor.duty_cycle_sp = -40
            if distance < 5:
                self.right_motor.duty_cycle_sp = 0
                self.left_motor.duty_cycle_sp = 0
                sleep(1)
                self.gripper.duty_cycle_sp = 50
                sleep(3)
                self.gripper.duty_cycle_sp = 0
                self.object_picked_up = True
        return BTStatus.SUCCESS
