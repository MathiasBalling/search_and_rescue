import time
from actuators import ActuatorsProposal, WheelCommand, TurnCommand
from ai.behaviors.behavior import Behavior
from sensors.colors import ColorSensors
from sensors.gyro import GyroSensor
from sensors.ultrasonic import UltrasonicSensor
from utils.blackboard import BlackBoard
from params import CAN_DETECTION_DISTANCE_THRESHOLD, TURN_TIME_PER_DEGREE,CAN_DETECTION_BASE_SPEED




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
        self.segment_start_monotonic = None

    def update(self):
        if self.blackboard["can_picked_up"]:
            self.weight = 0.0
            return
    
        if self.ultrasonic_sensor.get_value() < CAN_DETECTION_DISTANCE_THRESHOLD:
            self.weight = 0.0
            return

        last_time_line_seen = self.blackboard["last_time_line_seen"]
        if time.time() - last_time_line_seen < 1.0:
            self.weight = 0.0
            return
        else:
            self.weight = 1

    def actuators_proposal(self):
        current_time = time.monotonic()
        if self.segment_start_monotonic is None:
            self.segment_start_monotonic = current_time

        ccw, deg = self.scan_steps[self.scan_index]
        duration = TURN_TIME_PER_DEGREE * deg
        elapsed_time = current_time - self.segment_start_monotonic

        if elapsed_time < duration:
            if ccw:
                return ActuatorsProposal(WheelCommand(-CAN_DETECTION_BASE_SPEED, CAN_DETECTION_BASE_SPEED))
            else:
                return ActuatorsProposal(WheelCommand(CAN_DETECTION_BASE_SPEED, -CAN_DETECTION_BASE_SPEED))
        else:
            self.scan_index = (self.scan_index + 1) % len(self.scan_steps)
            self.segment_start_monotonic = current_time
            next_ccw,_ = self.scan_steps[self.scan_index]
            if next_ccw:
                return ActuatorsProposal(WheelCommand(-CAN_DETECTION_BASE_SPEED, CAN_DETECTION_BASE_SPEED))
            else:
                return ActuatorsProposal(WheelCommand(CAN_DETECTION_BASE_SPEED, -CAN_DETECTION_BASE_SPEED))