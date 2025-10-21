from behavior_tree import BTStatus, BTNode, BlackBoard
from robot import EV3Robot

from params import CAN_DETECTION_BASE_SPEED, CAN_DETECTION_DISTANCE_THRESHOLD, MOTOR_OFF


class CanDetection(BTNode):
    def __init__(self, robot: EV3Robot, blackboard: BlackBoard):
        self.robot = robot
        self.blackboard = blackboard
        self.can_found = False

    def detecting_can(self) -> bool:
        distance = self.robot.ultrasound_sensor.value() / 10
        self.robot.right_motor.duty_cycle_sp = CAN_DETECTION_BASE_SPEED
        self.robot.left_motor.duty_cycle_sp = -CAN_DETECTION_BASE_SPEED
        print("Distance to can:", distance, "cm")
        if distance < CAN_DETECTION_DISTANCE_THRESHOLD:
            self.robot.right_motor.duty_cycle_sp = MOTOR_OFF
            self.robot.left_motor.duty_cycle_sp = MOTOR_OFF
            self.can_found = True

        return self.can_found

    def tick(self) -> BTStatus:
        if self.detecting_can():
            return BTStatus.SUCCESS
        return BTStatus.FAILURE
