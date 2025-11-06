import time
from actuators import ActuatorsProposal,GripperCommand, WheelCommand
from ai.behaviors.behavior import Behavior
from params import CAN_DETECTION_DISTANCE_THRESHOLD
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
        if self.blackboard["can_picked_up"]:
            self.weight = 0.0
            return

        last_time_line_seen = self.blackboard["last_time_line_seem"]
        if time.time() - last_time_line_seen < 1.0:
            self.weight = 0.0
            return
        else:
            self.weight = 0.5

        ultra_value = self.ultrasonic_sensor.get_value()
        if ultra_value < CAN_DETECTION_DISTANCE_THRESHOLD:
            self.weight += 1

    def actuators_proposal(self):
        if self.ultrasonic_sensor.get_value() < 6:
            self.blackboard["can_picked_up"] = True
            return ActuatorsProposal(GripperCommand())

        return ActuatorsProposal(WheelCommand(20,20))
