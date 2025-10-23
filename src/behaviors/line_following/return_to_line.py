import time
from behavior_tree import BTStatus, BTNode
from blackboard import BlackBoard
from robot import EV3Robot
from pid_controller import PIDController

from params import RETURN_TO_LINE_BASE_SPEED


class ReturnToLine(BTNode):
    def __init__(self, robot: EV3Robot, blackboard: BlackBoard):
        self.robot = robot
        self.blackboard = blackboard

    def tick(self) -> BTStatus:
        self.robot.set_wheel_duty_cycles(left=RETURN_TO_LINE_BASE_SPEED, right=RETURN_TO_LINE_BASE_SPEED)
        left_color, right_color = self.robot.get_color_sensor_readings()
        if left_color > 30 and right_color <= 20:
            self.robot.set_wheel_duty_cycles(left=RETURN_TO_LINE_BASE_SPEED, right=-20)
            if left_color < 30 and right_color < 30:
                self.robot.set_wheel_duty_cycles(left=0, right=0)
                return BTStatus.SUCCESS
        elif right_color > 30 and left_color <= 20:
            self.robot.set_wheel_duty_cycles(left=-20, right=RETURN_TO_LINE_BASE_SPEED)
            if left_color < 30 and right_color < 30:
                self.robot.set_wheel_duty_cycles(left=0, right=0)
                return BTStatus.SUCCESS
        return BTStatus.RUNNING