from time import time
from behavior_tree import BTStatus, BTNode
from blackboard import BlackBoard
from robot import EV3Robot


class CanPickup(BTNode):
    def __init__(self, robot: EV3Robot, blackboard: BlackBoard):
        self.robot = robot
        self.blackboard = blackboard
        self.object_picked_up = False

    def tick(self) -> BTStatus:
        print("picking up can...")
        distance = self.robot.ultrasound_sensor.value() / 10
        print("Distance to can:", distance, "cm")
        self.robot.set_wheel_duty_cycles(left=40, right=40)
        if distance < 3:
            self.object_picked_up = True
            self.robot.set_wheel_duty_cycles(left=0, right=0)
            self.robot.close_gripper()
            print("Can picked up!")
            time.sleep(2)
            return BTStatus.SUCCESS
        return BTStatus.RUNNING
