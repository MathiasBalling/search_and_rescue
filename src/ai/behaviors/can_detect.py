import time
from actuators import ActuatorsProposal, WheelCommand
from ai.behaviors.behavior import Behavior
from sensors.colors import ColorSensors
from sensors.gyro import GyroSensor
from sensors.ultrasonic import UltrasonicSensor
from utils.blackboard import BlackBoard
from params import (
    CAN_DETECTION_DISTANCE_THRESHOLD,
    CAN_PICKED_UP,
    LAST_TIME_LINE_SEEN,
    TURN_TIME_PER_DEGREE,
    CAN_DETECTION_BASE_SPEED,
)

TURN_LEFT = WheelCommand(-CAN_DETECTION_BASE_SPEED, CAN_DETECTION_BASE_SPEED)
TURN_RIGHT = WheelCommand(CAN_DETECTION_BASE_SPEED, -CAN_DETECTION_BASE_SPEED)


class CanDetectionBehavior(Behavior):
    def __init__(
        self,
        blackboard: BlackBoard,
        color_sensors: ColorSensors,
        gyro: GyroSensor,
        ultrasonic_sensor: UltrasonicSensor,
    ):
        super().__init__(blackboard, 0.0)
        self.color_sensors = color_sensors
        self.gyro = gyro
        self.ultrasonic_sensor = ultrasonic_sensor
        self.scan_steps = [
            (True, 30.0),
            (False, 60.0),
            (True, 60.0),
            (False, 60.0),
        ]
        self.scan_index = 0
        self.turn_segment_start = None

    def update(self):
        if self.blackboard[CAN_PICKED_UP]:
            self.weight = 0.0
            return

        if self.ultrasonic_sensor.get_value() < CAN_DETECTION_DISTANCE_THRESHOLD:
            self.weight = 0.0
            return

        last_time_line_seen = self.blackboard[LAST_TIME_LINE_SEEN]
        if time.time() - last_time_line_seen < 1.0:
            self.weight = 0.0
            return

        self.weight = 1

    def actuators_proposal(self):
        current_time = time.monotonic()  # FIX: monotonic?????
        if self.turn_segment_start is None:
            self.turn_segment_start = current_time

        ccw, deg = self.scan_steps[self.scan_index]
        turn_duration = TURN_TIME_PER_DEGREE * deg
        elapsed_time = current_time - self.turn_segment_start

        if elapsed_time < turn_duration:
            if ccw:
                return ActuatorsProposal(TURN_LEFT)
            else:
                return ActuatorsProposal(TURN_RIGHT)
        else:
            self.scan_index = (self.scan_index + 1) % len(self.scan_steps)
            self.turn_segment_start = current_time
            next_ccw, _ = self.scan_steps[self.scan_index]

            if next_ccw:
                return ActuatorsProposal(TURN_LEFT)
            else:
                return ActuatorsProposal(TURN_RIGHT)

