import math
import time

from ai.behaviors.behavior import Behavior
from actuators import ActuatorsProposal, StopCommand, WheelCommand

from sensors.colors import ColorSensors
from sensors.gyro import GyroSensor
from sensors.pose import PoseSensor

from sensors.ultrasonic import UltrasonicSensor
from utils.blackboard import BlackBoard
from utils.pid_controller import PIDController


from params import (
    CAN_PICKED_UP,
    INTENSITY_LINE_THRESHOLD,
    LAST_TIME_LINE_SEEN,
    LINE_END_THRESHOLD,
    LINE_FOLLOWING_BASE_SPEED,
    LINE_FOLLOWING_TURN_SPEED_GAIN,
    INTENSITY_FLOOR_THRESHOLD,
    INTENSITY_PART_LINE_THRESHOLD,
    LINE_FOLLOWING_PID_KP,
    LINE_FOLLOWING_PID_KD,
    LINE_FOLLOWING_PID_KI,
    LINE_FOLLOWING_SHARP_TURN_SPEED,
    LINE_GAP_THRESHOLD,
    MAX_METERS_PER_SEC,
    TURN_ANGLE_THRESHOLD,
    deg_to_rad,
)

MODE_STRAIGHT = "straight"
MODE_UPHILL = "uphill"
MODE_DOWNHILL = "downhill"

STATE_FOLLOW = "follow"
STATE_TURN = "turn"


SHARP_LEFT_TURN = WheelCommand(
    left_speed=-LINE_FOLLOWING_SHARP_TURN_SPEED,
    right_speed=LINE_FOLLOWING_SHARP_TURN_SPEED,
)
SHARP_RIGHT_TURN = WheelCommand(
    left_speed=LINE_FOLLOWING_SHARP_TURN_SPEED,
    right_speed=-LINE_FOLLOWING_SHARP_TURN_SPEED,
)


class LineFollowingBehavior(Behavior):
    ############################################################
    # Required methods
    ############################################################
    def __init__(
        self,
        blackboard: BlackBoard,
        color_sensors: ColorSensors,
        ultrasonic_sensor: UltrasonicSensor,
        gyro: GyroSensor,
        pose: PoseSensor,
    ):
        super().__init__(blackboard, 1.0)  # 1.0 because we start on the line
        self.color_sensors = color_sensors
        self.gyro = gyro
        self.ultrasonic_sensor = ultrasonic_sensor
        self.pose = pose
        self.line_follow_pid = PIDController(
            LINE_FOLLOWING_PID_KP,
            LINE_FOLLOWING_PID_KI,
            LINE_FOLLOWING_PID_KD,
            (-MAX_METERS_PER_SEC, MAX_METERS_PER_SEC),
            0.0,
        )
        self.turn_pid = PIDController(
            0.2,
            0.02,
            0,
            (-LINE_FOLLOWING_SHARP_TURN_SPEED, LINE_FOLLOWING_SHARP_TURN_SPEED),
        )
        self.base_speed = LINE_FOLLOWING_BASE_SPEED

        self.controller_mode = MODE_STRAIGHT
        self.state = STATE_FOLLOW

        self.last_left_line_seen = 0
        self.last_right_line_seen = 0

        self.turn_angle_start = None
        self.turned_back = False

    def update(self):
        l_val, r_val = self.color_sensors.get_value()
        now = time.time()

        if (
            l_val < INTENSITY_PART_LINE_THRESHOLD
            or r_val < INTENSITY_PART_LINE_THRESHOLD
        ):
            self.blackboard[LAST_TIME_LINE_SEEN] = now

        if self.state != STATE_FOLLOW:
            # Very important we recover the line
            self.weight = 5.0
            return

        if now - self.blackboard[LAST_TIME_LINE_SEEN] > LINE_END_THRESHOLD:
            self.weight = 0.0
            return

        self.weight = 1.0

    def actuators_proposal(self):
        cmd = self.follow_line()
        return ActuatorsProposal(cmd)

    def follow_line(self):
        current_time = time.time()

        left_intensity, right_intensity = self.color_sensors.get_value()

        self.update_line_seen()

        # self.update_mode()

        diff = left_intensity - right_intensity

        control = self.line_follow_pid.compute(diff, current_time)

        distance_front = self.ultrasonic_sensor.get_value()

        base_speed = self.base_speed

        if abs(diff) > 0.3:
            base_speed = self.base_speed * LINE_FOLLOWING_TURN_SPEED_GAIN
        # elif distance_front < 30 and (
        #     left_intensity > INTENSITY_FLOOR_THRESHOLD
        #     and right_intensity > INTENSITY_FLOOR_THRESHOLD
        # ) and not self.blackboard[CAN_PICKED_UP]::
        elif distance_front < 30 and not self.blackboard[CAN_PICKED_UP]:
            # To now crash into the object
            print("Slowing down (ultrasonic value:", distance_front, ")")
            base_speed = self.base_speed * 0.2

        pid_left_control = base_speed - control
        pid_right_control = base_speed + control
        pid_left_control = min(
            max(-MAX_METERS_PER_SEC, pid_left_control), MAX_METERS_PER_SEC
        )
        pid_right_control = min(
            max(-MAX_METERS_PER_SEC, pid_right_control), MAX_METERS_PER_SEC
        )

        last_left_full_line_seen = current_time - self.last_left_line_seen
        last_right_full_line_seen = current_time - self.last_right_line_seen

        left_see_line = left_intensity < INTENSITY_PART_LINE_THRESHOLD
        right_see_line = right_intensity < INTENSITY_PART_LINE_THRESHOLD

        x, y, angle = self.pose.get_value()

        if self.state == STATE_FOLLOW:
            if (
                left_intensity <= INTENSITY_LINE_THRESHOLD
                and right_intensity <= INTENSITY_LINE_THRESHOLD
            ):
                # print("Black-Black")
                self.state = STATE_TURN

            if (
                left_intensity >= INTENSITY_FLOOR_THRESHOLD
                and right_intensity >= INTENSITY_FLOOR_THRESHOLD
                and (
                    LINE_GAP_THRESHOLD < last_left_full_line_seen < LINE_END_THRESHOLD
                    or LINE_GAP_THRESHOLD
                    < last_right_full_line_seen
                    < LINE_END_THRESHOLD
                )
            ):
                # print("White-White")
                self.state = STATE_TURN

        elif self.state == STATE_TURN:
            if self.turn_angle_start is None:
                self.turn_angle_start = angle

            if (left_see_line and not right_see_line) or (
                right_see_line and not left_see_line
            ):
                # print("Switching back")
                self.reset_turn_logic()
                self.state = STATE_FOLLOW

                return WheelCommand(
                    left_speed=pid_left_control, right_speed=pid_right_control
                )

            angle_turned = self.turn_angle_start - angle
            if abs(angle_turned) < TURN_ANGLE_THRESHOLD and not self.turned_back:
                # Turn
                if last_left_full_line_seen < last_right_full_line_seen:
                    self.turn_pid.setpoint = -TURN_ANGLE_THRESHOLD
                else:
                    self.turn_pid.setpoint = TURN_ANGLE_THRESHOLD
            else:
                self.turned_back = True
                self.turn_pid.setpoint = 0

                if abs(angle_turned) < deg_to_rad(0.5):
                    # Turn back
                    self.reset_turn_logic()
                    self.state = STATE_FOLLOW
                    return StopCommand()

            turn_ctrl = self.turn_pid.compute(angle_turned, time.time())

            return WheelCommand(turn_ctrl, -turn_ctrl)

        # If hard turn is not needed we use the PID control.
        return WheelCommand(left_speed=pid_left_control, right_speed=pid_right_control)

    def reset_turn_logic(self):
        self.turn_pid.reset()
        self.turn_angle_start = None
        self.turned_back = False

    ############################################################
    # Other methods
    ############################################################
    def update_line_seen(self):
        left, right = self.color_sensors.get_value()
        if left <= INTENSITY_LINE_THRESHOLD:
            self.last_left_line_seen = time.time()
        if right <= INTENSITY_LINE_THRESHOLD:
            self.last_right_line_seen = time.time()

    def set_controller_straight(self):
        if self.controller_mode == MODE_STRAIGHT:
            return
        self.line_follow_pid.kp = LINE_FOLLOWING_PID_KP
        self.line_follow_pid.ki = LINE_FOLLOWING_PID_KI
        self.line_follow_pid.kd = LINE_FOLLOWING_PID_KD
        self.controller_mode = MODE_STRAIGHT
        self.base_speed = LINE_FOLLOWING_BASE_SPEED
        self.line_follow_pid.reset()

    def set_controller_uphill(self):
        if self.controller_mode == MODE_UPHILL:
            return
        self.line_follow_pid.kp = 40.0
        self.line_follow_pid.ki = 0
        self.line_follow_pid.kd = 0
        self.controller_mode = MODE_UPHILL
        self.base_speed = 70
        self.line_follow_pid.reset()

    def update_mode(self):
        angle = self.gyro.get_value()
        if angle <= 15:
            self.set_controller_straight()
        else:
            self.set_controller_uphill()
        # print("Angle:", angle, "Mode:", self.controller_mode)
