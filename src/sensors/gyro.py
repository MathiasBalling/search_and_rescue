from sensors.sensor import Sensor
import ev3dev.ev3 as ev3


class GyroSensor(Sensor):
    __slots__ = ["sensor", "value"]

    def __init__(self):
        self.sensor = ev3.GyroSensor(ev3.INPUT_3)
        self.sensor.mode = ev3.GyroSensor.MODE_GYRO_RATE
        self.value = 0

    def update(self):
        self.value = self.sensor.value()

    def get_value(self):
        return self.value
