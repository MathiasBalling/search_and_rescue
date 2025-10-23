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
        self.returned_to_line = False
        self.right_on_line = False
        self.left_on_line = False
        self.both_on_line = False

    def tick(self) -> BTStatus:
        if self.blackboard["returned_to_line"]:
            return BTStatus.SUCCESS

        self.robot.open_gripper()
        left_color, right_color = self.robot.get_color_sensor_readings()
        print("Return to line - Left color:", left_color, "Right color:", right_color)
        if left_color >= 20 and right_color < 20:
            self.robot.set_wheel_duty_cycles(left=0, right=0)
            print("right black")
            self.right_on_line = True
            time.sleep(3)
            self.robot.set_wheel_duty_cycles(left=-30, right=RETURN_TO_LINE_BASE_SPEED)
        if right_color >= 20 and left_color < 20:
            self.robot.set_wheel_duty_cycles(left=0, right=0)
            print("left black")
            self.left_on_line = True
            time.sleep(3)
            self.robot.set_wheel_duty_cycles(left=RETURN_TO_LINE_BASE_SPEED, right=-30)
        if left_color < 20 and right_color < 20:
            print("on line")
            self.both_on_line = True
            self.robot.set_wheel_duty_cycles(left=0, right=0)
            time.sleep(5)
            return BTStatus.SUCCESS
        else:
            self.robot.set_wheel_duty_cycles(left=-RETURN_TO_LINE_BASE_SPEED, right=-RETURN_TO_LINE_BASE_SPEED)
            return BTStatus.RUNNING

