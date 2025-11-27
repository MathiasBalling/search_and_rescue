import time
from actuators import ActuatorsProposal, StopCommand, WheelCommand
from ai.behaviors.behavior import Behavior
from sensors.colors import ColorSensors
from sensors.gyro import GyroSensor
from sensors.pose import PoseSensor
from sensors.ultrasonic import UltrasonicSensor
from utils.blackboard import BlackBoard
from params import (
    CAN_ANGLE,
    CAN_DECTECTION_SCAN_DEGREES,
    CAN_PICKED_UP,
    LAST_TIME_LINE_SEEN,
    CAN_DETECTION_BASE_SPEED,
    LINE_END_THRESHOLD,
    MAX_METERS_PER_SEC,
    POINTING_AT_CAN,
    deg_to_rad,
)
from utils.pid_controller import PIDController

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

    def find_center(self, measurement: Measurement):
        idx = self._measurements.index(measurement)
        max_left, max_right = idx, idx
        while (
            abs(
                self._measurements[max_left].distance
                - self._measurements[max_left - 1].distance
            )
            < 1.0
        ):
            max_left -= 1
        while (
            abs(
                self._measurements[max_right].distance
                - self._measurements[max_right + 1].distance
            )
            < 1.0
        ):
            max_right += 1

        left_measure = self._measurements[max_left]
        right_measure = self._measurements[max_right]

        center = (left_measure.angle + right_measure.angle) / 2
        return center

    def find_lowest_dist(self) -> Measurement:
        return min(self._measurements, key=lambda m: m.distance)

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
        self.pid = PIDController(
            0.2, 0.0, 0.0, (-MAX_METERS_PER_SEC, MAX_METERS_PER_SEC)
        )

        self.start_angle = None
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
            return ActuatorsProposal(StopCommand())

        x, y, angle = self.pose.get_value()
        if self.start_angle is None:
            self.start_angle = angle
        dist = self.ultrasonic_sensor.get_value()
        # print("Dist:", dist, "Angle:", angle)

        angle_turned = self.start_angle - angle
        if self.scan_step_index == SCAN_TURN_LEFT:
            if angle_turned < -CAN_DECTECTION_SCAN_DEGREES / 2:
                self.scan_step_index = SCAN_TURN_RIGHT
                return ActuatorsProposal(StopCommand())
            else:
                return ActuatorsProposal(TURN_LEFT)
        elif self.scan_step_index == SCAN_TURN_RIGHT:
            if angle_turned > CAN_DECTECTION_SCAN_DEGREES / 2:
                self.scan_step_index = SCAN_TURN_TO_BEST
                return ActuatorsProposal(StopCommand())
            else:
                self.measurements.add(Measurement(dist, angle_turned))
                return ActuatorsProposal(TURN_RIGHT)
        elif self.scan_step_index == SCAN_TURN_TO_BEST:
            if self.can_angle is None:
                # FIX: Find groups instead and choose the best
                best = self.measurements.find_best()
                print("Best angle:", best.angle, best.distance, best.weight)
                center = self.measurements.find_center(best)
                # lowest = self.measurements.find_lowest_dist()
                # print("lowest dist:", lowest.angle, lowest.distance, lowest.weight)
                self.can_angle = center
                self.blackboard[CAN_ANGLE] = self.can_angle
                self.pid.setpoint = self.can_angle

            control = self.pid.compute(angle_turned, time.time())
            if abs(self.can_angle - angle_turned) > deg_to_rad(1):
                self.blackboard[POINTING_AT_CAN] = False
                return ActuatorsProposal(WheelCommand(control, -control))
            else:
                self.blackboard[POINTING_AT_CAN] = True
                return ActuatorsProposal(StopCommand())

        else:
            print("Unknown scan step index:", self.scan_step_index)
            return ActuatorsProposal(StopCommand())

    def reset(self):
        self.start_angle = None
        self.can_angle = None
        self.scan_step_index = 0
        self.measurements.reset()
        self.pid.reset()
