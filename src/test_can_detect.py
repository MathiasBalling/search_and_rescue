#!/usr/bin/env python3
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

    # Add sensors to the controller
    controller.add_sensor(color_sensors)
    controller.add_sensor(gyro_sensor)
    controller.add_sensor(ultrasonic_sensor)

    # Create behaviors
    can_detect_behavior = CanDetectionBehavior(
        blackboard=blackboard,
        color_sensors=color_sensors,
        gyro=gyro_sensor,
        ultrasonic_sensor=ultrasonic_sensor,
    )

    # Add behaviors to the controller
    controller.add_behavior(can_detect_behavior)

    # Run the controller forever
    controller.run()


if __name__ == "__main__":
    main()
