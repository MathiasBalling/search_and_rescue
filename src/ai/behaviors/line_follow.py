import time

from ai.behaviors.behavior import Behavior
from actuators import ActuatorsProposal, WheelCommand

from sensors.colors import ColorSensors
from sensors.gyro import GyroSensor

from utils.blackboard import BlackBoard
from utils.pid_controller import PIDController


from params import (
    INTENSITY_LINE_THRESHOLD,
    LAST_TIME_LINE_SEEN,
    LINE_FOLLOWING_BASE_SPEED,
    LINE_FOLLOWING_SHARP_TURN_SPEED_BACK,
    LINE_FOLLOWING_TURN_SPEED_GAIN,
    INTENSITY_FLOOR_THRESHOLD,
    INTENSITY_PART_LINE_THRESHOLD,
    LINE_FOLLOWING_PID_KP,
    LINE_FOLLOWING_PID_KD,
    LINE_FOLLOWING_PID_KI,
    LINE_FOLLOWING_SHARP_TURN_SPEED,
)

MODE_STRAIGHT = "straight"
MODE_UPHILL = "uphill"
MODE_DOWNHILL = "downhill"

STATE_FOLLOW = "follow"
STATE_TURN = "turn"


SHARP_LEFT_TURN = WheelCommand(
    left_speed=LINE_FOLLOWING_SHARP_TURN_SPEED_BACK,
    right_speed=LINE_FOLLOWING_SHARP_TURN_SPEED,
)
SHARP_RIGHT_TURN = WheelCommand(
    left_speed=LINE_FOLLOWING_SHARP_TURN_SPEED,
    right_speed=LINE_FOLLOWING_SHARP_TURN_SPEED_BACK,
)


class LineFollowingBehavior(Behavior):
    ############################################################
    # Required methods
    ############################################################
    def __init__(
        self, blackboard: BlackBoard, color_sensors: ColorSensors, gyro: GyroSensor
    ):
        super().__init__(blackboard, 1.0)  # 1.0 because we start on the line
        self.color_sensors = color_sensors
        self.gyro = gyro
        self.limits = (-100, 100)
        self.pid = PIDController(
            LINE_FOLLOWING_PID_KP,
            LINE_FOLLOWING_PID_KI,
            LINE_FOLLOWING_PID_KD,
            self.limits,
        )
        self.controller_mode = MODE_STRAIGHT
        self.state = STATE_FOLLOW
        self.base_speed = LINE_FOLLOWING_BASE_SPEED

        self.last_left_line_seen = 0
        self.last_right_line_seen = 0

    def update(self):
        l_val, r_val = self.color_sensors.get_value()
        now = time.time()

        if (
            l_val < INTENSITY_PART_LINE_THRESHOLD
            or r_val < INTENSITY_PART_LINE_THRESHOLD
        ):
            self.blackboard[LAST_TIME_LINE_SEEN] = now
        # print(
        #     "Last time line seen: {}, {},{}".format(
        #         now - self.blackboard[LAST_TIME_LINE_SEEN], l_val, r_val
        # )

        if now - self.blackboard[LAST_TIME_LINE_SEEN] > 1.0:
            self.weight = 0.0
            return

        self.weight = 1.0

    def actuators_proposal(self):
        # TODO: PID scale output with curve
        cmd = self.follow_line()
        return ActuatorsProposal(cmd)

    def follow_line(self):
        current_time = time.time()

        left_intensity, right_intensity = self.color_sensors.get_value()

        self.update_line_seen()

        # self.update_mode()

        diff = left_intensity - right_intensity

        control = self.pid.compute(diff, current_time)

        base_speed = (
            self.base_speed
            if abs(diff) < 0.3
            else self.base_speed * LINE_FOLLOWING_TURN_SPEED_GAIN
        )

        left_control = base_speed - control
        right_control = base_speed + control

        left_control = round(min(max(self.limits[0], left_control), self.limits[1]))
        right_control = round(min(max(self.limits[0], right_control), self.limits[1]))

        # print(
        #     # "PID control",
        #     # control,
        #     # left_control,
        #     # right_control,
        #     # "Colors:",
        #     # left_intensity,
        #     # right_intensity,
        # )

        last_left = current_time - self.last_left_line_seen
        last_right = current_time - self.last_right_line_seen
        print(
            "time:",
            current_time,
            "left_intensity:",
            left_intensity,
            "right_intensity:",
            right_intensity,
        )

        if self.state == STATE_FOLLOW:
            if (
                left_intensity <= INTENSITY_LINE_THRESHOLD
                and right_intensity >= INTENSITY_FLOOR_THRESHOLD
            ) or (
                left_intensity >= INTENSITY_FLOOR_THRESHOLD
                and right_intensity <= INTENSITY_LINE_THRESHOLD
            ):
                # Possible corner
                self.state = STATE_TURN
            # if (
            #     left_intensity >= INTENSITY_FLOOR_THRESHOLD
            #     and right_intensity >= INTENSITY_FLOOR_THRESHOLD
            # ):
            #     time_lost = last_left if last_left < last_right else last_right
            #
            #     if 0.5 < time_lost < 1.0:
            #         # Possible corner
            #         self.state = STATE_TURN

        elif self.state == STATE_TURN:
            if (
                left_intensity <= INTENSITY_PART_LINE_THRESHOLD
                or right_intensity <= INTENSITY_PART_LINE_THRESHOLD
            ):
                self.state = STATE_FOLLOW
            else:
                if last_left < last_right:
                    return SHARP_LEFT_TURN
                else:
                    return SHARP_RIGHT_TURN

        # If hard turn is not needed we use the PID control.
        return WheelCommand(left_speed=left_control, right_speed=right_control)

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
        self.pid.kp = LINE_FOLLOWING_PID_KP
        self.pid.ki = LINE_FOLLOWING_PID_KI
        self.pid.kd = LINE_FOLLOWING_PID_KD
        self.controller_mode = MODE_STRAIGHT
        self.base_speed = LINE_FOLLOWING_BASE_SPEED
        self.pid.reset()

    def set_controller_uphill(self):
        if self.controller_mode == MODE_UPHILL:
            return
        self.pid.kp = 2.5
        self.pid.ki = 0
        self.pid.kd = 0
        self.controller_mode = MODE_UPHILL
        self.base_speed = 70
        self.pid.reset()

    def update_mode(self):
        angle = self.gyro.get_value()
        if angle <= 15:
            self.set_controller_straight()
        else:
            self.set_controller_uphill()
        # print("Angle:", angle, "Mode:", self.controller_mode)
