from sensors.sensor import Sensor
import ev3dev.ev3 as ev3

MAX_REFLECT = 29  # White
MIN_REFLECT = 3  # Black


class ColorSensors(Sensor):
    __slots__ = ["left_sensor", "right_sensor", "left_value", "right_value"]

    def __init__(self):
        self.left_sensor = ev3.ColorSensor(ev3.INPUT_1)
        assert self.left_sensor.connected
        self.left_sensor.mode = ev3.ColorSensor.MODE_COL_REFLECT

        self.right_sensor = ev3.ColorSensor(ev3.INPUT_4)
        assert self.right_sensor.connected
        self.right_sensor.mode = ev3.ColorSensor.MODE_COL_REFLECT

        self.left_value = 100
        self.right_value = 100

    def update(self):
        self.left_value = (self.left_sensor.value() - MIN_REFLECT) / (
            MAX_REFLECT - MIN_REFLECT
        )
        self.left_value = max(0.0, min(1.0, self.left_value))
        self.right_value = (self.right_sensor.value() - MIN_REFLECT) / (
            MAX_REFLECT - MIN_REFLECT
        )
        self.right_value = max(0.0, min(1.0, self.right_value))

    def get_value(self):
        return (self.left_value, self.right_value)
