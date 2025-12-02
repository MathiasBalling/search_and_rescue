#!/usr/bin/env python3
from actuators import Actuators
from ai.behaviors.can_pickup import CanPickupBehavior
from ai.controller import Controller
from params import setup_blackboard
from sensors.colors import ColorSensors
from sensors.pose import PoseSensor
from sensors.ultrasonic import UltrasonicSensor


def main():
    actuators = Actuators()
    controller = Controller(actuators)
    blackboard = setup_blackboard()

    # Create sensors
    color_sensors = ColorSensors()
    ultrasonic_sensor = UltrasonicSensor()
    mL, mR = actuators.get_wheel_motors()
    pose_sensor = PoseSensor(mL, mR)

    # Add sensors to the controller
    controller.add_sensor(color_sensors)
    controller.add_sensor(ultrasonic_sensor)
    controller.add_sensor(pose_sensor)

    # Create behaviors

    can_pickup_behavior = CanPickupBehavior(
        blackboard=blackboard,
        color_sensors=color_sensors,
        ultrasonic_sensor=ultrasonic_sensor,
        pose=pose_sensor,
    )

    # Add behaviors to the controller
    controller.add_behavior(can_pickup_behavior)

    # Run the controller forever
    controller.run()


if __name__ == "__main__":
    main()
