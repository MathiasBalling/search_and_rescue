from sensors.sensor import Sensor
import ev3dev.ev3 as ev3


class GyroSensor(Sensor):
    __slots__ = ["sensor", "value"]

    def __init__(self):
        self.sensor = ev3.GyroSensor(ev3.INPUT_3)
        assert self.sensor.connected
        # FIX: Update this to angle or angle+rate instead of rate
        # Or use rate and calculate the angle ourselves

        # self.sensor.mode = ev3.GyroSensor.MODE_GYRO_G_A
        # self.sensor.mode = ev3.GyroSensor.MODE_GYRO_RATE
        self.sensor.mode = ev3.GyroSensor.MODE_GYRO_ANG
        self.offset = None
        self.value = 0

    def update(self):
        if self.offset is None:
            # Assume we start on a straight surface.
            self.offset = self.sensor.value()
        self.value = self.sensor.value() - self.offset

    def get_value(self):
        return self.value
