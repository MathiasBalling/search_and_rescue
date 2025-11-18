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
            (False, 60.0),
            (True, 60.0),
            (False, 60.0),
        ]
        self.scan_sequence_index = 0
        self.turn_segment_start = None
        self.skip_first_after_init = False
        self.deg = 30
        self.ccw = True

    def update(self):
        self.weight = 0.5
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
        else:
            self.weight += 0.5


    def actuators_proposal(self):
        current_time = time.time()
        if self.turn_segment_start is None:
            self.turn_segment_start = current_time

        turn_duration = TURN_TIME_PER_DEGREE * deg
        elapsed_time = current_time - self.turn_segment_start

        if elapsed_time < turn_duration:
            if self.skip_first_after_init:
                ccw, deg = self.scan_steps[self.scan_sequence_index]
                self.turn_segment_start = current_time
                self.scan_sequence_index + 1
                self.scan_sequence_index %= 3
                if ccw:
                    return ActuatorsProposal(TURN_LEFT)
                else:
                    return ActuatorsProposal(TURN_RIGHT)
                
            self.skip_first_after_init = True
            if ccw:
                return ActuatorsProposal(TURN_LEFT)
            else:
                return ActuatorsProposal(TURN_RIGHT)
        
        

        # current_time = time.time()
        # self.skip_first_after_init
        # if self.turn_segment_start is None:
        #     self.turn_segment_start = current_time

        # ccw, deg = self.scan_steps[self.scan_sequence_index]
        # turn_duration = TURN_TIME_PER_DEGREE * deg
        # elapsed_time = current_time - self.turn_segment_start

        # if elapsed_time < turn_duration:
        #     if ccw:
        #         return ActuatorsProposal(TURN_LEFT)
        #     else:
        #         return ActuatorsProposal(TURN_RIGHT)
        # else:
        #     self.scan_sequence_index = (self.scan_sequence_index + 1) % len(self.scan_steps)
        #     self.turn_segment_start = current_time
        #     next_ccw, _ = self.scan_steps[self.scan_sequence_index]

        #     if next_ccw:
        #         return ActuatorsProposal(TURN_LEFT)
        #     else:
        #         return ActuatorsProposal(TURN_RIGHT)

