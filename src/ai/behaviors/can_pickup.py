import time
from actuators import ActuatorsProposal
from ai.behaviors.behavior import Behavior
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
        last_time_line_seen = self.blackboard["last_time_line_seem"]
        ultra_value = self.ultrasonic_sensor.get_value()
        if time.time() - last_time_line_seen < 1.0:
            self.weight = 0.0
            return
        else:
            self.weight = 0.5

        if ultra_value < self.CAN_DETECTION_DISTANCE_THRESHOLD:
            self.weight += 1
            return

    def get_control_proposal(self):
        # TODO:
        return ActuatorsProposal(0, 0, False)
