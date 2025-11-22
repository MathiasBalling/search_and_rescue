#!/usr/bin/env python3
from actuators import Actuators
from ai.behaviors.can_detect import CanDetectionBehavior
from ai.behaviors.can_pickup import CanPickupBehavior
from ai.behaviors.line_follow import LineFollowingBehavior
from ai.behaviors.line_return import LineReturnBehavior
from ai.controller import Controller
from params import setup_blackboard
from sensors.colors import ColorSensors
from sensors.gyro import GyroSensor
from sensors.pose import PoseSensor
from sensors.ultrasonic import UltrasonicSensor


def main():
    actuators = Actuators()
    controller = Controller(actuators)
    blackboard = setup_blackboard()

    # Create sensors
    color_sensors = ColorSensors()
    gyro_sensor = GyroSensor()
    ultrasonic_sensor = UltrasonicSensor()
    mL, mR = actuators.get_wheel_motors()
    pose_sensor = PoseSensor(mL, mR)

    # Add sensors to the controller
    controller.add_sensor(color_sensors)
    controller.add_sensor(gyro_sensor)
    controller.add_sensor(ultrasonic_sensor)
    controller.add_sensor(pose_sensor)

    # Create behaviors
    line_following_behavior = LineFollowingBehavior(
        blackboard=blackboard,
        color_sensors=color_sensors,
        gyro=gyro_sensor,
        pose=pose_sensor,
    )

    line_return_behavior = LineReturnBehavior(
        blackboard=blackboard, color_sensors=color_sensors, pose=pose_sensor
    )

    can_detect_behavior = CanDetectionBehavior(
        blackboard=blackboard,
        color_sensors=color_sensors,
        gyro=gyro_sensor,
        ultrasonic_sensor=ultrasonic_sensor,
        pose=pose_sensor,
    )

    can_pickup_behavior = CanPickupBehavior(
        blackboard=blackboard,
        color_sensors=color_sensors,
        gyro=gyro_sensor,
        ultrasonic_sensor=ultrasonic_sensor,
        pose=pose_sensor,
    )

    # logging = Logging(blackboard, color_sensors, gyro_sensor, ultrasonic_sensor)

    # Add behaviors to the controller
    controller.add_behavior(line_following_behavior)
    controller.add_behavior(line_return_behavior)
    controller.add_behavior(can_detect_behavior)
    controller.add_behavior(can_pickup_behavior)
    # controller.add_behavior(logging)

    # Run the controller forever
    controller.run()


if __name__ == "__main__":
    main()
