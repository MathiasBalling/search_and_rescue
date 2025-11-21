#!/usr/bin/env python3
import time
from ai.behaviors.can_detect import CanDetectionBehavior
from ai.controller import Controller
from params import setup_blackboard
from sensors.colors import ColorSensors
from sensors.gyro import GyroSensor
from sensors.ultrasonic import UltrasonicSensor


def main():
    controller = Controller()
    blackboard = setup_blackboard()

    # Create sensors
    color_sensors = ColorSensors()
    gyro_sensor = GyroSensor()
    ultrasonic_sensor = UltrasonicSensor()

    while True:
        color_sensors.update()
        time.sleep(0.02)


if __name__ == "__main__":
    main()
