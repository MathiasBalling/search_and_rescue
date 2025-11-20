import time
from actuators import ActuatorsProposal, WheelCommand
from ai.behaviors.behavior import Behavior
from sensors.colors import ColorSensors
from sensors.gyro import GyroSensor
from sensors.ultrasonic import UltrasonicSensor
from utils.blackboard import BlackBoard
from params import (
    CAN_DECTECTION_SCAN_DEGREES,
    CAN_DETECTION_DISTANCE_THRESHOLD,
    CAN_PICKED_UP,
    CAN_SIDE_PICKUP,
    LAST_TIME_LINE_SEEN,
    TURN_TIME_PER_DEGREE,
    CAN_DETECTION_BASE_SPEED,
    CAN_PICKUP_MAX_DISTANCE,
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
            (False, CAN_DECTECTION_SCAN_DEGREES * 2),
            (True, CAN_DECTECTION_SCAN_DEGREES * 2),
        ]
        self.scan_sequence_index = 0
        self.turn_segment_start = None
        self.first_turn_done = False
        self.deg = CAN_DECTECTION_SCAN_DEGREES
        self.ccw = True

    def update(self):
        if self.blackboard[CAN_PICKED_UP]:
            self.weight = 0.0
            return

        if (
            CAN_PICKUP_MAX_DISTANCE
            < self.ultrasonic_sensor.get_value()
            < CAN_DETECTION_DISTANCE_THRESHOLD
        ):
            self.weight = 0.0
            return

        self.weight = 0.5

        last_time_line_seen = self.blackboard[LAST_TIME_LINE_SEEN]
        if time.time() - last_time_line_seen < 1.0:
            self.weight = 0.0
            return
        else:
            self.weight += 0.5

    def actuators_proposal(self):
        if self.blackboard[CAN_PICKED_UP]:
            return ActuatorsProposal(WheelCommand(0, 0))

        current_time = time.time()
        if self.turn_segment_start is None:
            self.turn_segment_start = current_time

        turn_duration = TURN_TIME_PER_DEGREE * self.deg
        elapsed_time = current_time - self.turn_segment_start
        if self.deg == CAN_DECTECTION_SCAN_DEGREES:
            current_deg = elapsed_time / TURN_TIME_PER_DEGREE
            self.blackboard[CAN_SIDE_PICKUP] = (current_deg, True)
        elif self.ccw:
            current_deg = CAN_DECTECTION_SCAN_DEGREES - (
                elapsed_time / TURN_TIME_PER_DEGREE
            )
            self.blackboard[CAN_SIDE_PICKUP] = (current_deg, True)
        else:
            current_deg = CAN_DECTECTION_SCAN_DEGREES - (
                elapsed_time / TURN_TIME_PER_DEGREE
            )
            self.blackboard[CAN_SIDE_PICKUP] = (current_deg, False)

        if elapsed_time >= turn_duration:
            if not self.first_turn_done:
                self.first_turn_done = True
                self.ccw, self.deg = self.scan_steps[self.scan_sequence_index]
                self.turn_segment_start = current_time
            else:
                self.scan_sequence_index = (self.scan_sequence_index + 1) % 2
                self.ccw, self.deg = self.scan_steps[self.scan_sequence_index]
                self.turn_segment_start = current_time

        if self.ccw:
            return ActuatorsProposal(TURN_LEFT)
        else:
            return ActuatorsProposal(TURN_RIGHT)
