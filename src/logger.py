import time
from actuators import ActuatorsProposal, WheelCommand
from ai.behaviors.behavior import Behavior
from params import INTENSITY_FLOOR_THRESHOLD
from sensors.colors import ColorSensors
from sensors.ultrasonic import UltrasonicSensor
from utils.blackboard import BlackBoard

from ev3dev2.power import PowerSupply

from datetime import datetime
import os


class Logging(Behavior):
    def __init__(
        self,
        blackboard: BlackBoard,
        color_sensors: ColorSensors,
        ultrasonic_sensor: UltrasonicSensor,
    ):
        super().__init__(blackboard, 0.0)
        self.color_sensors = color_sensors
        self.ultrasonic_sensor = ultrasonic_sensor
        self.power = PowerSupply()

        # Logging
        log_dir = "/home/robot/log"
        os.makedirs(log_dir, exist_ok=True)
        log_filename = datetime.now().strftime("%Y-%m-%d_%H-%M-%S.csv")
        self.log_file = open(os.path.join(log_dir, log_filename), "w")

        self.log_file.write(
            "time,voltage,current,intensity_left,intensity_right,on_line,distance_front,slope_angle\n"
        )
        # print("Logging to {}".format(log_filename))

    def update(self):
        # Always 0
        self.weight = 0.0
        now = time.time()
        voltage = self.power.measured_voltage
        current = self.power.measured_current
        intensity_left, intensity_right = self.color_sensors.get_value()
        on_line = (
            True
            if intensity_left < INTENSITY_FLOOR_THRESHOLD
            or intensity_right < INTENSITY_FLOOR_THRESHOLD
            else False
        )
        distance_front = self.ultrasonic_sensor.get_value()

        self.log_file.write(
            "{},{},{},{},{},{},{},{}\n".format(
                now,
                voltage,
                current,
                intensity_left,
                intensity_right,
                on_line,
                distance_front,
                slope_angle,
            )
        )
        # print("Logged data at time {}".format(now))

    def actuators_proposal(self) -> ActuatorsProposal:
        return ActuatorsProposal(WheelCommand(0, 0))
