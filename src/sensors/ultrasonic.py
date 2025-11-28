from sensors.sensor import Sensor
import ev3dev.ev3 as ev3


class UltrasonicSensor(Sensor):
    __slots__ = ["sensor", "value"]

    def __init__(self):
        self.sensor = ev3.UltrasonicSensor(ev3.INPUT_2)
        assert self.sensor.connected
        self.sensor.mode = ev3.UltrasonicSensor.MODE_US_DIST_CM
        self.sensor.mode = (
            ev3.UltrasonicSensor.MODE_US_SI_CM
        )  # TODO: Maybe use this mode?
        self.value = 0

    def update(self):
        self.value = self.sensor.distance_centimeters

    def get_value(self):
        return self.value
