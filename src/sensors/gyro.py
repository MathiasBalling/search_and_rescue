from sensors.sensor import Sensor
import ev3dev2.sensor.lego as sensor
from collections import deque


class GyroSensor(Sensor):
    __slots__ = ["sensor", "value"]

    def __init__(self):
        self.sensor = sensor.GyroSensor()
        self.sensor.reset()
        self.sensor.calibrate()

        self.sensor.mode = sensor.GyroSensor.MODE_GYRO_ANG
        self.value = 0
        # comment test
        self.updates = 0
        self._last_values = deque(maxlen=50)

    def update(self):
        if self.updates % 50 == 0 and self.updates > 0:
            # Update offset if all in _last_values is under 3
            if all(x < 5 for x in self._last_values):
                print("Updating gyro offset:", self.sensor.value())
                self.offset = self.sensor.reset()

        self.value = self.sensor.value()
        self._last_values.append(self.value)
        self.updates += 1

    def get_value(self):
        print("Gyro value:", self.value)
        return self.value
