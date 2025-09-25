import time
from behavior_tree import BTStatus, BTNode
from robot import EV3Robot
from pid_controller import PIDController

BASE_SPEED = 70


class LineFollowing(BTNode):
    def __init__(self, robot: EV3Robot):
        self.robot = robot
        self.pid = PIDController(
            kp=1, ki=0.2, kd=0.1, setpoint=0, output_limits=(-100, 100)
        )
        self.pid_turn = PIDController(
            kp=4, ki=0.0, kd=1.5, setpoint=0, output_limits=(-100, 100)
        )
        self._last_time_line_seen = time.time()

    def tick(self) -> BTStatus:
        left_color, right_color = self.robot.get_color_sensor_readings()
        current_time = time.time()

        print(
            "Sensor readings",
            left_color,
            right_color,
        )

        if left_color > 20 and right_color > 20:
            self.robot.left_motor.duty_cycle_sp = 0
            self.robot.right_motor.duty_cycle_sp = 0

            control = self.pid.compute(left_color - right_color, current_time)

            left_control = BASE_SPEED - control
            right_control = BASE_SPEED + control

            left_control = min(max(0, left_control), 100)
            right_control = min(max(0, right_control), 100)

            self.robot.left_motor.duty_cycle_sp = -left_control
            self.robot.right_motor.duty_cycle_sp = -right_control
        else:
            # If we lose the line, turn in place to try and find it
            turn_control = self.pid_turn.compute(left_color - right_color, current_time)

            self.robot.left_motor.duty_cycle_sp = turn_control
            self.robot.right_motor.duty_cycle_sp = -turn_control

        return BTStatus.RUNNING
