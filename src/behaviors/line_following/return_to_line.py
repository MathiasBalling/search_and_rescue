from behavior_tree import BTStatus, BTNode
from blackboard import BlackBoard
from robot import EV3Robot


class ReturnToLine(BTNode):
    def __init__(self, robot: EV3Robot, blackboard: BlackBoard):
        self.robot = robot
        self.blackboard = blackboard
        self.returned_to_line = False
        self.did_turn = False

    def tick(self) -> BTStatus:
        if self.blackboard["returned_to_line"]:
            return BTStatus.SUCCESS

        if not self.did_turn:
            self.robot.turn_deg(180)
            self.did_turn = True

        left_color, right_color = self.robot.get_color_sensor_readings()
        print("Return to line - Left color:", left_color, "Right color:", right_color)
        if left_color < 20 or right_color < 20:
            self.robot.set_wheel_duty_cycles(left=0, right=0)
            self.robot.open_gripper()
            self.blackboard["returned_to_line"] = True
            return BTStatus.SUCCESS
        return BTStatus.RUNNING
