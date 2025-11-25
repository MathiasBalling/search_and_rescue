from sensors.sensor import Sensor
import ev3dev.ev3 as ev3
from collections import deque


class GyroSensor(Sensor):
    __slots__ = ["sensor", "value"]

    def __init__(self):
        self.sensor = ev3.GyroSensor(ev3.INPUT_3)
        assert self.sensor.connected

        self.sensor.mode = ev3.GyroSensor.MODE_GYRO_ANG
        self.offset = None
        self.value = 0

        self.updates = 0
        self._last_values = deque(maxlen=100)

    def update(self):
        if self.offset is None:
            # Assume we start on a straight surface.
            self.offset = self.sensor.value()

        if self.updates % 100 == 0 and self.updates > 0:
            # Update offset if all in _last_values is under 3
            if all(abs(x) < 5 for x in self._last_values):
                print("Updating gyro offset:", self.sensor.value())
                self.offset = self.sensor.value()

        self.value = self.sensor.value() - self.offset
        # print(self.sensor.value())
        print("Gyro value:", self.value)
        self._last_values.append(self.value)
        self.updates += 1

    def get_value(self):
        return self.value
