import time
from actuators import (
    ActuatorsProposal,
    GripperCommand,
    WheelCommand,
    WheelGripperCommand,
)
from ai.behaviors.behavior import Behavior
from params import (
    CAN_DETECTION_DISTANCE_THRESHOLD,
    CAN_PICKED_UP,
    CAN_PICKUP_BASE_SPEED,
    CAN_PICKUP_MAX_DISTANCE,
    LAST_TIME_LINE_SEEN,
)
from sensors.colors import ColorSensors
from sensors.gyro import GyroSensor
from sensors.ultrasonic import UltrasonicSensor
from utils.blackboard import BlackBoard


class CanPickupBehavior(Behavior):
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

    def update(self):
        if self.blackboard[CAN_PICKED_UP]:
            self.weight = 0.0
            return

        last_time_line_seen = self.blackboard[LAST_TIME_LINE_SEEN]
        if time.time() - last_time_line_seen < 1.0:
            self.weight = 0.0
            return

        self.weight = 0.4

        ultra_value = self.ultrasonic_sensor.get_value()
        if ultra_value < CAN_DETECTION_DISTANCE_THRESHOLD:
            self.weight += 0.5

        if ultra_value < CAN_PICKUP_MAX_DISTANCE:
            self.weight += 0.5

    def actuators_proposal(self):
        if self.ultrasonic_sensor.get_value() < CAN_PICKUP_MAX_DISTANCE:
            self.blackboard[CAN_PICKED_UP] = True
            return ActuatorsProposal(GripperCommand())
            # Do this if we don't hit the can with the gripper
            # return ActuatorsProposal(WheelGripperCommand(10, 10))

        if self.ultrasonic_sensor.get_value() < CAN_DETECTION_DISTANCE_THRESHOLD:
            return ActuatorsProposal(
                WheelCommand(CAN_PICKUP_BASE_SPEED, CAN_PICKUP_BASE_SPEED)
            )

        # Something must be wrong in can detection
        return ActuatorsProposal(WheelCommand(0, 0))
