import ev3dev.ev3 as ev3
from ev3dev2.sound import Sound


class EV3Robot:
    __slots__ = (
        "left_motor",
        "right_motor",
        "left_color_sensor",
        "right_color_sensor",
        "gripper_motor",
        "ultrasound_sensor",
        "speaker",
    )

    def __init__(self):
        # Set up motors
        self.left_motor = ev3.LargeMotor(ev3.OUTPUT_A)
        self.right_motor = ev3.LargeMotor(ev3.OUTPUT_D)
        # self.gripper_motor = ev3.MediumMotor(ev3.OUTPUT_C)
        self.left_motor.run_direct()
        self.right_motor.run_direct()
        # self.gripper_motor.run_direct()

        assert self.left_motor.connected, "Left motor is not connected to port A"
        assert self.right_motor.connected, "Right motor is not connected to port B"
        # assert self.gripper_motor.connected, "Gripper motor is not connected to port C"

        # Set up sensors
        self.left_color_sensor = ev3.ColorSensor(ev3.INPUT_1)
        self.right_color_sensor = ev3.ColorSensor(ev3.INPUT_4)
        self.left_color_sensor.mode = ev3.ColorSensor.MODE_COL_REFLECT
        self.right_color_sensor.mode = ev3.ColorSensor.MODE_COL_REFLECT
        # self.ultrasound_sensor = ev3.UltrasonicSensor(ev3.INPUT_2)
        # self.ultrasound_sensor.mode = "US-DIST-CM"

        assert self.right_color_sensor.connected, (
            "Right color sensor 1 is not connected to port 4"
        )
        assert self.left_color_sensor.connected, (
            "Left color sensor 2 is not connected to port 1"
        )
        # assert self.ultrasound_sensor.connected, (
        #     "Ultrasound sensor is not connected to port 2"
        # )

        # Set up sound
        self.speaker = Sound()
        self.speaker.speak("bing bong")

    def get_color_sensor_readings(self):
        return (self.left_color_sensor.value(), self.right_color_sensor.value())
