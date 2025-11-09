from sensors.sensor import Sensor
import ev3dev.ev3 as ev3


class GyroSensor(Sensor):
    __slots__ = ["sensor", "value"]

    def __init__(self):
        self.sensor = ev3.GyroSensor(ev3.INPUT_3)
        # FIX: Update this to angle or angle+rate instead of rate
        # Or use rate and calculate the angle ourselves
        self.sensor.mode = ev3.GyroSensor.MODE_GYRO_G_A
        self.sensor.mode = ev3.GyroSensor.MODE_GYRO_RATE
        self.value = 0

    def update(self):
        self.value = self.sensor.value()

    def get_value(self):
        return self.value
