import time
from actuators import ActuatorsProposal, WheelCommand
from ai.behaviors.behavior import Behavior
from params import LINE_INTENSITY_WHITE_THRESHOLD, LLR, P_GAIN, SPEED_MODE
from sensors.colors import ColorSensors
from sensors.gyro import GyroSensor
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
        gyro: GyroSensor,
        ultrasonic_sensor: UltrasonicSensor,
    ):
        super().__init__(blackboard, 0.0)
        self.color_sensors = color_sensors
        self.gyro = gyro
        self.ultrasonic_sensor = ultrasonic_sensor
        self.power = PowerSupply()

        # Logging
        log_dir = "/home/robot/log/{}_{}".format(
            self.blackboard[P_GAIN], self.blackboard[SPEED_MODE]
        )
        os.makedirs(log_dir, exist_ok=True)
        log_filename = datetime.now().strftime("%Y-%m-%d_%H-%M-%S.csv")
        self.log_file = open(os.path.join(log_dir, log_filename), "w")

        self.log_file.write("time,p_gain,speed_mode,voltage,current,LLR\n")
        # print("Logging to {}".format(log_filename))
        self.start_time = time.time()
        self.measurements = []

    def update(self):
        # Always 0
        self.weight = 0.0
        duration = time.time() - self.start_time
        voltage = self.power.measured_voltage
        current = self.power.measured_current
        distance_front = self.ultrasonic_sensor.get_value()
        self.measurements.append((duration, voltage, current, self.blackboard[LLR]))

        if distance_front <= 6:
            for measurement in self.measurements:
                self.log_file.write(
                    "{},{},{},{},{},{}\n".format(
                        measurement[0],
                        self.blackboard[P_GAIN],
                        self.blackboard[SPEED_MODE],
                        measurement[1],
                        measurement[2],
                        measurement[3],
                    )
                )

            exit()

    def actuators_proposal(self) -> ActuatorsProposal:
        return ActuatorsProposal(WheelCommand(0, 0))
