import time
from behavior_tree import BTStatus, BTNode
from blackboard import BlackBoard
from robot import EV3Robot

from params import (
    CAN_DETECTION_BASE_SPEED,
    CAN_DETECTION_DISTANCE_THRESHOLD,
    TURN_TIME_PER_DEGREE,
)


class CanDetection(BTNode):
    def __init__(self, robot: EV3Robot, blackboard: BlackBoard):
        self.robot = robot
        self.blackboard = blackboard
        self.can_found = False
        self.turn_counter = 0
        self.turn_duration = 20
        self.turned_right = False
        self.start_right_turn = None

    def tick(self) -> BTStatus:
        if self.can_found:
            return BTStatus.SUCCESS

        if self.start_right_turn is None:
            self.start_right_turn = time.time()

        distance = self.robot.get_ultrasound_sensor_reading()
        if distance <= CAN_DETECTION_DISTANCE_THRESHOLD:
            self.can_found = True
        else:
            # Turn right or left based on current state
            if not self.turned_right:
                # Turn right
                self.robot.set_wheel_duty_cycles(
                    left=CAN_DETECTION_BASE_SPEED, right=-CAN_DETECTION_BASE_SPEED
                )
                if time.time() - self.start_right_turn > 1.0:
                    self.turned_right = True
            else:
                self.robot.set_wheel_duty_cycles(
                    left=-CAN_DETECTION_BASE_SPEED, right=CAN_DETECTION_BASE_SPEED
                )

            print("Distance to can detection:", distance, "cm")

        return BTStatus.RUNNING
