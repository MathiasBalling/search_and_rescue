#!/usr/bin/env python3
from ai.behaviors.line_follow import LineFollowingBehavior
from logger import Logging
from ai.controller import Controller
from params import P_GAIN, SPEED_MODE, setup_blackboard
from sensors.colors import ColorSensors
from sensors.gyro import GyroSensor
from sensors.ultrasonic import UltrasonicSensor


def main():
    controller = Controller()
    blackboard = setup_blackboard()
    blackboard[SPEED_MODE] = "aggressive"
    blackboard[P_GAIN] = 2.5

    # Create sensors
    color_sensors = ColorSensors()
    gyro_sensor = GyroSensor()
    ultrasonic_sensor = UltrasonicSensor()

    # Add sensors to the controller
    controller.add_sensor(color_sensors)
    controller.add_sensor(gyro_sensor)
    controller.add_sensor(ultrasonic_sensor)

    # Create behaviors
    line_following_behavior = LineFollowingBehavior(
        blackboard=blackboard, color_sensors=color_sensors, gyro=gyro_sensor
    )

    logger = Logging(blackboard, color_sensors, gyro_sensor, ultrasonic_sensor)

    # Add behaviors to the controller
    controller.add_behavior(line_following_behavior)
    controller.add_behavior(logger)

    # Run the controller forever
    controller.run()


if __name__ == "__main__":
    main()
