from math import cos, pi, sin
from params import WHEEL_CIRCUMFERENCE, WHEEL_SEPARATION
from sensors.sensor import Sensor


class PoseSensor(Sensor):
    __slots__ = ["sensor", "value"]

    def __init__(self, left_motor, right_motor):
        self.left_motor = left_motor
        self.right_motor = right_motor

        self.left_motor.position = 0
        self.right_motor.position = 0

        self.x = 0
        self.y = 0
        self.angle = 0

        self.last_left_position = 0
        self.last_right_position = 0

    def update(self):
        d_l_position = self.left_motor.position - self.last_left_position
        d_r_position = self.right_motor.position - self.last_right_position

        self.last_left_position = self.left_motor.position
        self.last_right_position = self.right_motor.position

        N_l = d_l_position / self.left_motor.count_per_rot
        N_r = d_r_position / self.right_motor.count_per_rot

        D_l = N_l * WHEEL_CIRCUMFERENCE
        D_r = N_r * WHEEL_CIRCUMFERENCE
        D_avg = (D_l + D_r) / 2
        d_angle = (D_r - D_l) / WHEEL_SEPARATION

        self.angle = self.angle + d_angle
        # if self.angle > pi:
        #     self.angle -= 2 * pi
        # elif self.angle < -pi:
        #     self.angle += 2 * pi

        d_x = D_avg * cos(self.angle)
        d_y = D_avg * sin(self.angle)

        self.x += d_x
        self.y += d_y

    def get_value(self):
        return (self.x, self.y, self.angle)
