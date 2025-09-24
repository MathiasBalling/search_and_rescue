import ev3dev.ev3 as ev3
from ev3dev2.sound import Sound


class EV3Robot:
    __slots__ = (
        "left_motor",
        "right_motor",
        "left_color_sensor",
        "right_color_sensor",
        "touch_sensor",
        "speaker",
    )

    def __init__(self):
        # Set up motors
        self.left_motor = ev3.LargeMotor(ev3.OUTPUT_A)
        self.right_motor = ev3.LargeMotor(ev3.OUTPUT_B)
        self.left_motor.run_direct()
        self.right_motor.run_direct()
        assert self.left_motor.connected, "Left motor is not connected to port A"
        assert self.right_motor.connected, "Right motor is not connected to port B"

        # Set up sensors
        self.right_color_sensor = ev3.ColorSensor(ev3.INPUT_1)
        self.left_color_sensor = ev3.ColorSensor(ev3.INPUT_2)
        self.left_color_sensor.mode = "COL-COLOR"
        self.right_color_sensor.mode = "COL-COLOR"
        assert self.right_color_sensor.connected, (
            "Right color sensor 1 is not connected to port 1"
        )
        assert self.left_color_sensor.connected, (
            "Left color sensor 2 is not connected to port 2"
        )

        # Set up touch sensor
        self.touch_sensor = ev3.TouchSensor(ev3.INPUT_3)
        assert self.touch_sensor.connected, "Touch sensor is not connected to port 3"

        # Set up sound
        # self.speaker = Sound()
        # self.speaker.speak("death and destruction to all perkere")

    def get_color_sensor_readings(self):
        return (self.left_color_sensor.value(), self.right_color_sensor.value())
