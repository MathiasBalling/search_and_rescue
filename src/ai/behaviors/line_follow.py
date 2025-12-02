import time

from ai.behaviors.behavior import Behavior
from actuators import ActuatorsProposal, StopCommand, WheelCommand

from sensors.colors import ColorSensors
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
    ULTRA_SOUND_THRESHOLD,
)

MODE_STRAIGHT = "straight"
MODE_UPHILL = "uphill"
MODE_DOWNHILL = "downhill"

STATE_FOLLOW = "follow"
STATE_LINE_RECOVER = "turn"


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
        pose: PoseSensor,
    ):
        super().__init__(blackboard, 1.0)  # 1.0 because we start on the line
        self.color_sensors = color_sensors
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

        self.last_left_part_line_seen = 0
        self.last_right_part_line_seen = 0
        self.last_middle_part_line_seen = 0
        self.last_left_line_seen = 0
        self.last_right_line_seen = 0
        self.last_middle_line_seen = 0

        self.turn_angle_start = None
        self.turn_angle_target = None
        self.turning_back = False

    def update(self):
        l_val, m_val, r_val = self.color_sensors.get_value()
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

        left_intensity, middle_intensity, right_intensity = (
            self.color_sensors.get_value()
        )

        self.update_part_line_seen()

        diff = left_intensity - right_intensity

        control = self.line_follow_pid.compute(diff, current_time)

        distance_front = self.ultrasonic_sensor.get_value()

        base_speed = self.base_speed

        min_gap_time = LINE_GAP_THRESHOLD
        max_gap_time = LINE_END_THRESHOLD

        if middle_intensity > 0.8:
            base_speed = self.base_speed * LINE_FOLLOWING_TURN_SPEED_GAIN
            min_gap_time = LINE_GAP_THRESHOLD
            max_gap_time = LINE_END_THRESHOLD
        # elif (
        #     distance_front < ULTRA_SOUND_THRESHOLD
        #     and (
        #         left_intensity > INTENSITY_FLOOR_THRESHOLD
        #         and right_intensity > INTENSITY_FLOOR_THRESHOLD
        #     )
        #     and not self.blackboard[CAN_PICKED_UP]
        # ):
        #     # To now crash into the object
        #     # print("Slowing down (ultrasonic value:", distance_front, ")")
        #     base_speed = self.base_speed * 0.2
        #     min_gap_time = LINE_GAP_THRESHOLD
        #     max_gap_time = LINE_END_THRESHOLD * 2
        #     # print("Wall detected, slowing down")

        pid_left_control = base_speed - control
        pid_right_control = base_speed + control
        pid_left_control = min(
            max(-MAX_METERS_PER_SEC, pid_left_control), MAX_METERS_PER_SEC
        )
        pid_right_control = min(
            max(-MAX_METERS_PER_SEC, pid_right_control), MAX_METERS_PER_SEC
        )

        last_left_line_seen = current_time - self.last_left_line_seen
        last_right_line_seen = current_time - self.last_right_line_seen
        last_middle_line_seen = current_time - self.last_middle_line_seen

        x, y, angle = self.pose.get_value()

        if self.state == STATE_FOLLOW:
            if (
                left_intensity >= INTENSITY_FLOOR_THRESHOLD
                and right_intensity >= INTENSITY_FLOOR_THRESHOLD
                and middle_intensity >= INTENSITY_FLOOR_THRESHOLD
                and (
                    min_gap_time < last_left_line_seen < max_gap_time
                    or min_gap_time < last_right_line_seen < max_gap_time
                    or min_gap_time < last_middle_line_seen < max_gap_time
                )
            ):
                # print("White-White")
                self.state = STATE_LINE_RECOVER
            return WheelCommand(
                left_speed=pid_left_control, right_speed=pid_right_control
            )

        elif self.state == STATE_LINE_RECOVER:
            if self.turn_angle_start is None:
                self.turn_angle_start = angle

            if self.only_one_see_line():
                # print("Switching back")
                self.reset_turn_logic()
                self.state = STATE_FOLLOW
                # print("Following line")
                return WheelCommand(
                    left_speed=pid_left_control, right_speed=pid_right_control
                )

            angle_turned = self.turn_angle_start - angle
            if abs(angle_turned) < TURN_ANGLE_THRESHOLD and not self.turning_back:
                # Turn
                if self.turn_angle_target is None:
                    if last_left_line_seen < last_right_line_seen:
                        self.turn_angle_target = -TURN_ANGLE_THRESHOLD
                    else:
                        self.turn_angle_target = TURN_ANGLE_THRESHOLD
                    self.turn_pid.setpoint = self.turn_angle_target
            else:
                self.turning_back = True
                self.turn_pid.setpoint = 0

                if abs(angle_turned) < deg_to_rad(1):
                    # Turn back
                    self.reset_turn_logic()
                    self.state = STATE_FOLLOW
                    return StopCommand()

            turn_ctrl = self.turn_pid.compute(angle_turned, time.time())

            return WheelCommand(turn_ctrl, -turn_ctrl)
        else:
            # print("Unknown state:", self.state)
            self.state = STATE_FOLLOW
            return StopCommand()

    def reset_turn_logic(self):
        self.turn_pid.reset()
        self.turn_angle_start = None
        self.turn_angle_target = None
        self.turning_back = False

    def one_see_line(self):
        left, middle, right = self.color_sensors.get_value()
        return (
            left < INTENSITY_FLOOR_THRESHOLD
            or middle < INTENSITY_FLOOR_THRESHOLD
            or right < INTENSITY_FLOOR_THRESHOLD
        )

    def only_one_see_line(self):
        left, middle, right = self.color_sensors.get_value()
        count = 0
        if left < INTENSITY_FLOOR_THRESHOLD:
            count += 1
        if right < INTENSITY_FLOOR_THRESHOLD:
            count += 1
        if middle < INTENSITY_FLOOR_THRESHOLD:
            count += 1
        return count == 1

    def min_two_see_line(self):
        left, middle, right = self.color_sensors.get_value()
        count = 0
        if left < INTENSITY_FLOOR_THRESHOLD:
            count += 1
        if right < INTENSITY_FLOOR_THRESHOLD:
            count += 1
        if middle < INTENSITY_FLOOR_THRESHOLD:
            count += 1
        return count >= 2

    def update_part_line_seen(self):
        left, middle, right = self.color_sensors.get_value()
        now = time.time()
        if left <= INTENSITY_PART_LINE_THRESHOLD:
            self.last_left_part_line_seen = now
        if right <= INTENSITY_PART_LINE_THRESHOLD:
            self.last_right_part_line_seen = now
        if middle <= INTENSITY_PART_LINE_THRESHOLD:
            self.last_middle_part_line_seen = now
        if left <= INTENSITY_FLOOR_THRESHOLD:
            self.last_left_line_seen = now
        if right <= INTENSITY_FLOOR_THRESHOLD:
            self.last_right_line_seen = now
        if middle <= INTENSITY_FLOOR_THRESHOLD:
            self.last_middle_line_seen = now
