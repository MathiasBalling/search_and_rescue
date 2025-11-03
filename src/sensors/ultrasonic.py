from sensors.sensor import Sensor
import ev3dev.ev3 as ev3


class UltrasonicSensor(Sensor):
    __slots__ = ["sensor", "value"]

    def __init__(self):
        self.sensor = ev3.UltrasonicSensor(ev3.INPUT_2)
        self.sensor.mode = ev3.UltrasonicSensor.MODE_US_DIST_CM
        self.value = 0

    def update(self):
        self.value = self.sensor.value() / 10.0

    def get_value(self):
        return self.value
