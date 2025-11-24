from math import cos, pi, sin
from params import WHEEL_CIRCUMFERENCE, WHEEL_SEPARATION
from sensors.sensor import Sensor


class PoseSensor(Sensor):
    __slots__ = ["sensor", "value"]

    def __init__(self, left_motor, right_motor):
        self.left_motor = left_motor
        self.right_motor = right_motor

        self.x = 0
        self.y = 0
        self.theta = 0

        self.last_left_position = self.left_motor.position
        self.last_right_position = self.right_motor.position

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
        d_theta = (D_r - D_l) / WHEEL_SEPARATION

        self.theta = self.theta + d_theta
        # if self.theta > pi:
        #     self.theta -= 2 * pi
        # elif self.theta < -pi:
        #     self.theta += 2 * pi

        d_x = D_avg * cos(self.theta)
        d_y = D_avg * sin(self.theta)

        self.x += d_x
        self.y += d_y

    def get_value(self):
        return (self.x, self.y, self.theta)
