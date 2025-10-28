from behavior_tree import BTStatus, BTNode
from blackboard import BlackBoard
from robot import EV3Robot

from params import (
    CAN_DETECTION_BASE_SPEED,
    CAN_DETECTION_DISTANCE_THRESHOLD,
)


class CanDetection(BTNode):
    def __init__(self, robot: EV3Robot, blackboard: BlackBoard):
        self.robot = robot
        self.blackboard = blackboard
        self.can_found = False
        self.turn_counter = 0
        self.turn_duration = 20
        self.turning_right = True

    def tick(self) -> BTStatus:
        if self.can_found:
            return BTStatus.SUCCESS

        distance = self.robot.get_ultrasound_sensor_reading()
        if distance <= CAN_DETECTION_DISTANCE_THRESHOLD:
            self.robot.set_wheel_duty_cycles(
                left=CAN_DETECTION_BASE_SPEED, right=CAN_DETECTION_BASE_SPEED
            )
            self.can_found = True
        else:
            # Zigzag search pattern
            self.turn_counter += 1
            
            # Switch direction after turn_duration ticks
            if self.turn_counter >= self.turn_duration:
                self.turning_right = not self.turning_right
                self.turn_counter = 0
            
            # Turn right or left based on current state
            if self.turning_right:
                # Turn right
                self.robot.turn_deg(30)
            else:
                # Turn left
                self.robot.turn_deg(30, False)
            
            print("Distance to can detection:", distance, "cm")

        return BTStatus.RUNNING
