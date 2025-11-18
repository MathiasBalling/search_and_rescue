#!/usr/bin/env python3
from ai.behaviors.can_detect import CanDetectionBehavior
from ai.controller import Controller
from logger import Logging
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

    # Add sensors to the controller
    controller.add_sensor(color_sensors)
    controller.add_sensor(gyro_sensor)
    controller.add_sensor(ultrasonic_sensor)

    # Create behaviors
    logger = Logging(blackboard, color_sensors, gyro_sensor, ultrasonic_sensor)

    # Add behaviors to the controller
    controller.add_behavior(logger)

    # Run the controller forever
    controller.run()


if __name__ == "__main__":
    main()
