from behavior_tree import BTStatus, BTNode
from blackboard import BlackBoard
from robot import EV3Robot


class CanPickup(BTNode):
    def __init__(self, robot: EV3Robot, blackboard: BlackBoard):
        self.robot = robot
        self.blackboard = blackboard
        self.object_picked_up = False

    def tick(self) -> BTStatus:
        if not self.object_picked_up:
            distance = self.robot.ultrasound_sensor.value() / 10
            print("Distance to can:", distance, "cm")
            self.robot.set_wheel_duty_cycles(left=40, right=40)
            if distance < 5:
                self.robot.set_wheel_duty_cycles(left=0, right=0)
                self.robot.close_gripper()
                # sleep(1)
                # self.robot.gripper_motor.duty_cycle_sp = 30
                # sleep(3)
                # self.robot.gripper_motor.duty_cycle_sp = 0
                self.object_picked_up = True
            else:
                return BTStatus.RUNNING
        return BTStatus.SUCCESS
