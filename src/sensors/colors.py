from sensors.sensor import Sensor
import ev3dev.ev3 as ev3

MIN_REFLECT_COLOR = 3  # Black
MAX_REFLECT_COLOR = 25  # White
MIN_REFLECT_LIGHT = 30  # Black
MAX_REFLECT_LIGHT = 50  # White


class ColorSensors(Sensor):
    __slots__ = [
        "left_sensor",
        "right_sensor",
        "left_value",
        "right_value",
        "middle_sensor",
        "middle_value",
    ]

    def __init__(self):
        self.left_sensor = ev3.ColorSensor(ev3.INPUT_1)
        assert self.left_sensor.connected
        self.left_sensor.mode = ev3.ColorSensor.MODE_COL_REFLECT

        self.right_sensor = ev3.ColorSensor(ev3.INPUT_4)
        assert self.right_sensor.connected
        self.right_sensor.mode = ev3.ColorSensor.MODE_COL_REFLECT

        self.middle_sensor = ev3.LightSensor(ev3.INPUT_3)
        assert self.middle_sensor.connected
        self.middle_sensor.mode = ev3.LightSensor.MODE_REFLECT

        self.left_value = 1
        self.right_value = 1
        self.middle_value = 1

    def update(self):
        self.left_value = (self.left_sensor.value() - MIN_REFLECT_COLOR) / (
            MAX_REFLECT_COLOR - MIN_REFLECT_COLOR
        )
        self.left_value = max(0.0, min(1.0, self.left_value))

        self.right_value = (self.right_sensor.value() - MIN_REFLECT_COLOR) / (
            MAX_REFLECT_COLOR - MIN_REFLECT_COLOR
        )
        self.right_value = max(0.0, min(1.0, self.right_value))

        self.middle_value = (
            self.middle_sensor.reflected_light_intensity - MIN_REFLECT_LIGHT
        ) / (MAX_REFLECT_LIGHT - MIN_REFLECT_LIGHT)
        self.middle_value = max(0.0, min(1.0, self.middle_value))

    def get_value(self):
        return (self.left_value, self.middle_value, self.right_value)
