import time
from actuators import (
    ActuatorsProposal,
    StopCommand,
    WheelCommand,
    WheelGripperCommand,
)
from ai.behaviors.behavior import Behavior
from params import (
    CAN_PICKUP_DISTANCE_THRESHOLD,
    CAN_PICKED_UP,
    CAN_PICKUP_BASE_SPEED,
    CAN_PICKUP_GRIP_SPEED,
    CAN_PICKUP_MAX_DISTANCE,
    LAST_TIME_LINE_SEEN,
    POINTING_AT_CAN,
)
from sensors.colors import ColorSensors
from sensors.pose import PoseSensor
from sensors.ultrasonic import UltrasonicSensor
from utils.blackboard import BlackBoard


class CanPickupBehavior(Behavior):
    def __init__(
        self,
        blackboard: BlackBoard,
        color_sensors: ColorSensors,
        ultrasonic_sensor: UltrasonicSensor,
        pose: PoseSensor,
    ):
        super().__init__(blackboard, 0.0)
        self.color_sensors = color_sensors
        self.pose = pose
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
        if ultra_value <= CAN_PICKUP_DISTANCE_THRESHOLD:
            self.weight += 0.5

        if ultra_value <= CAN_PICKUP_MAX_DISTANCE:
            self.weight += 0.5

        if self.blackboard[POINTING_AT_CAN]:
            self.weight += 5.0

    def actuators_proposal(self):
        dist = self.ultrasonic_sensor.get_value()
        if self.blackboard[CAN_PICKED_UP]:
            return ActuatorsProposal(StopCommand())

        # print("dist:", dist)
        if (
            dist <= CAN_PICKUP_MAX_DISTANCE or dist == 255
        ):  # Too close to detect the can
            self.blackboard[CAN_PICKED_UP] = True
            return ActuatorsProposal(
                WheelGripperCommand(CAN_PICKUP_GRIP_SPEED, CAN_PICKUP_GRIP_SPEED)
            )

        if dist <= CAN_PICKUP_DISTANCE_THRESHOLD or self.blackboard[POINTING_AT_CAN]:
            return ActuatorsProposal(
                WheelCommand(CAN_PICKUP_BASE_SPEED, CAN_PICKUP_BASE_SPEED)
            )

        # Something must be wrong in can detection
        print("Something must be wrong in can detection, dist:", dist)
        return ActuatorsProposal(StopCommand())
