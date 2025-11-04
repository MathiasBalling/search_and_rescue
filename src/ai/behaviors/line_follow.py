import time
from actuators import ActuatorsProposal
from ai.behaviors.behavior import Behavior
from params import (
    LINE_FOLLOWING_PID_KD,
    LINE_FOLLOWING_PID_KI,
    LINE_FOLLOWING_PID_KP,
    LINE_INTENSITY_THRESHOLD,
)
from sensors.colors import ColorSensors
from sensors.gyro import GyroSensor
from utils.blackboard import BlackBoard
from utils.pid_controller import PIDController


class LineFollowingBehavior(Behavior):
    def __init__(
        self, blackboard: BlackBoard, color_sensors: ColorSensors, gyro: GyroSensor
    ):
        super().__init__(blackboard, 1.0)  # 1.0 because we start on the line
        self.color_sensors = color_sensors
        self.gyro = gyro
        self.pid = PIDController(
            LINE_FOLLOWING_PID_KP,
            LINE_FOLLOWING_PID_KI,
            LINE_FOLLOWING_PID_KD,
            (-100, 100),
        )

    def update(self):
        l_val, r_val = self.color_sensors.get_value()
        if l_val < LINE_INTENSITY_THRESHOLD or r_val < LINE_INTENSITY_THRESHOLD:
            self.blackboard["last_time_line_seem"] = time.time()

        self.weight = 0.0

    def get_control_proposal(self):
        # TODO:
        return ActuatorsProposal(0, 0, False)
