import time
from actuators import ActuatorsProposal, StopCommand, WheelCommand
from ai.behaviors.behavior import Behavior
from sensors.colors import ColorSensors
from sensors.gyro import GyroSensor
from sensors.pose import PoseSensor
from sensors.ultrasonic import UltrasonicSensor
from utils.blackboard import BlackBoard
from params import (
    CAN_DECTECTION_SCAN_DEGREES,
    CAN_PICKED_UP,
    LAST_TIME_LINE_SEEN,
    CAN_DETECTION_BASE_SPEED,
    LINE_END_THRESHOLD,
    deg_to_rad,
)

TURN_LEFT = WheelCommand(-CAN_DETECTION_BASE_SPEED, CAN_DETECTION_BASE_SPEED)
TURN_RIGHT = WheelCommand(CAN_DETECTION_BASE_SPEED, -CAN_DETECTION_BASE_SPEED)


SCAN_TURN_LEFT = 0
SCAN_TURN_RIGHT = 1
SCAN_TURN_TO_BEST = 2


class Measurement:
    __slots__ = ["distance", "angle", "weight"]

    def __init__(self, distance, angle):
        self.distance = distance
        self.angle = angle
        # Higher weight for closer distance and angle near 0
        self.weight = (
            1.0 / (1.0 + abs(self.distance)) * (1.0 / (1.0 + abs(self.angle / 5)))
        )


class Measurements:
    __slots__ = ["_measurements"]

    def __init__(self):
        self._measurements = []

    def add(self, measurement: Measurement):
        self._measurements.append(measurement)

    def find_best(self) -> Measurement:
        return max(self._measurements, key=lambda m: m.weight)

    def reset(self):
        self._measurements = []


class CanDetectionBehavior(Behavior):
    def __init__(
        self,
        blackboard: BlackBoard,
        color_sensors: ColorSensors,
        gyro: GyroSensor,
        ultrasonic_sensor: UltrasonicSensor,
        pose: PoseSensor,
    ):
        super().__init__(blackboard, 0.0)
        self.color_sensors = color_sensors
        self.gyro = gyro
        self.pose = pose
        self.ultrasonic_sensor = ultrasonic_sensor

        self.start_angle = None
        self.target_deg = CAN_DECTECTION_SCAN_DEGREES / 2
        self.measurements = Measurements()
        self.can_angle = None
        self.scan_step_index = 0

    def update(self):
        self.weight = 0.0
        if self.blackboard[CAN_PICKED_UP]:
            return

        if time.time() - self.blackboard[LAST_TIME_LINE_SEEN] < LINE_END_THRESHOLD:
            self.reset()
            # We saw the line recently
            return
        else:
            self.weight += 0.5

        if self.can_angle is None:
            self.weight += 1.0
        elif self.start_angle is not None:
            x, y, angle = self.pose.get_value()
            angle_turned = self.start_angle - angle
            if abs(self.can_angle - angle_turned) > 1:
                self.weight += 1.0

    def actuators_proposal(self):
        if self.blackboard[CAN_PICKED_UP]:
            return ActuatorsProposal(StopCommand)

        x, y, angle = self.pose.get_value()
        if self.start_angle is None:
            self.start_angle = angle
        dist = self.ultrasonic_sensor.get_value()
        print("Dist:", dist, "Angle:", angle)

        angle_turned = self.start_angle - angle
        if self.scan_step_index == SCAN_TURN_LEFT:
            if angle_turned < -CAN_DECTECTION_SCAN_DEGREES / 2:
                self.scan_step_index = SCAN_TURN_RIGHT
                return ActuatorsProposal(StopCommand)
            else:
                self.measurements.add(Measurement(dist, angle_turned))
                return ActuatorsProposal(TURN_LEFT)
        elif self.scan_step_index == SCAN_TURN_RIGHT:
            if angle_turned > CAN_DECTECTION_SCAN_DEGREES / 2:
                self.scan_step_index = SCAN_TURN_TO_BEST
                return ActuatorsProposal(StopCommand)
            else:
                self.measurements.add(Measurement(dist, angle_turned))
                return ActuatorsProposal(TURN_RIGHT)
        elif self.scan_step_index == SCAN_TURN_TO_BEST:
            if self.can_angle is None:
                best = self.measurements.find_best()
                print("Best angle:", best.angle, best.distance, best.weight)
                # for m in self.measurements._measurements:
                #     print(m.distance, m.angle, m.weight)
                self.can_angle = best.angle

            if abs(self.can_angle - angle_turned) < deg_to_rad(2):
                return ActuatorsProposal(StopCommand)
            elif (self.can_angle - angle_turned) < 0:
                return ActuatorsProposal(TURN_LEFT)
            else:
                return ActuatorsProposal(TURN_RIGHT)
        else:
            print("Unknown scan step index:", self.scan_step_index)
            return ActuatorsProposal(StopCommand)

    def reset(self):
        self.start_angle = None
        self.target_deg = CAN_DECTECTION_SCAN_DEGREES / 2
        self.can_angle = None
        self.scan_step_index = 0
        self.measurements.reset()
