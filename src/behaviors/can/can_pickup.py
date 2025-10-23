import time
from behavior_tree import BTStatus, BTNode
from blackboard import BlackBoard
from params import MOTOR_OFF
from robot import EV3Robot


class CanPickup(BTNode):
    def __init__(self, robot: EV3Robot, blackboard: BlackBoard):
        self.robot = robot
        self.blackboard = blackboard

    def tick(self) -> BTStatus:
        can_picked_up = self.blackboard["can_picked_up"]
        if can_picked_up:
            return BTStatus.SUCCESS

        distance = self.robot.get_ultrasound_sensor_reading()
        self.robot.set_wheel_duty_cycles(left=40, right=40)
        if distance < 6:
            self.blackboard["can_picked_up"] = True
            self.robot.set_wheel_duty_cycles(left=15, right=15)
            self.robot.close_gripper()
            time.sleep(2)
            self.robot.set_wheel_duty_cycles(left=MOTOR_OFF, right=MOTOR_OFF)
            return BTStatus.SUCCESS
        return BTStatus.RUNNING
