import time
from behavior_tree import BTStatus, BTNode
from blackboard import BlackBoard
from robot import EV3Robot

from params import (
    CAN_DETECTION_BASE_SPEED,
    CAN_DETECTION_DISTANCE_THRESHOLD,
    MOTOR_OFF,
    CAN_PICKUP_BASE_SPEED,
)


class CanDetection(BTNode):
    def __init__(self, robot: EV3Robot, blackboard: BlackBoard):
        self.robot = robot
        self.blackboard = blackboard
        self.can_found = False
        self.can_picked_up = False

    def tick(self) -> BTStatus:
        if self.can_picked_up:
            return BTStatus.SUCCESS

        if self.can_found:
            if self.robot.can_pickup():
                self.can_picked_up = True
                return BTStatus.SUCCESS
            else:
                return BTStatus.RUNNING

        distance = self.robot.get_ultrasound_sensor_reading()
        if distance <= CAN_DETECTION_DISTANCE_THRESHOLD:
            self.robot.set_wheel_duty_cycles(left=20, right=20)
            self.can_found = True
            print("Can detected!")
            time.sleep(1)
        else:
            self.robot.set_wheel_duty_cycles(
                left=-CAN_DETECTION_BASE_SPEED, right=CAN_DETECTION_BASE_SPEED
            )
            print("Distance to can detection:", distance, "cm")

        return BTStatus.RUNNING
