from sensors.sensor import Sensor
import ev3dev.ev3 as ev3


class ColorSensors(Sensor):
    __slots__ = ["left_sensor", "right_sensor", "left_value", "right_value"]

    def __init__(self):
        self.left_sensor = ev3.ColorSensor(ev3.INPUT_1)
        self.left_sensor.mode = ev3.ColorSensor.MODE_COL_REFLECT

        self.right_sensor = ev3.ColorSensor(ev3.INPUT_4)
        self.right_sensor.mode = ev3.ColorSensor.MODE_COL_REFLECT

        self.left_value = 0
        self.right_value = 0

    def update(self):
        self.left_value = self.left_sensor.value()
        self.right_value = self.right_sensor.value()

    def get_value(self):
        return (self.left_value, self.right_value)
