# General parameters
import time
from utils.blackboard import BlackBoard
import math


def dps_to_mps(dps):
    return dps * math.pi / 180.0 * WHEEL_RADIUS


def mps_to_dps(mps):
    dps = mps * 180.0 / math.pi / WHEEL_RADIUS
    return round(max(-MAX_DEGREES_PER_SEC, min(dps, MAX_DEGREES_PER_SEC)))


def deg_to_rad(deg) -> float:
    return deg * math.pi / 180.0


def rad_to_deg(rad) -> float:
    return rad * 180.0 / math.pi


DT = 0.02

MOTOR_OFF = 0
GRIPPER_SPEED = 100

# Robot parameters
WHEEL_RADIUS = 0.0275
WHEEL_CIRCUMFERENCE = WHEEL_RADIUS * 2 * math.pi
WHEEL_SEPARATION = 0.125
MAX_DEGREES_PER_SEC = 900
MAX_METERS_PER_SEC = dps_to_mps(MAX_DEGREES_PER_SEC)


INTENSITY_FLOOR_THRESHOLD = 0.9
INTENSITY_PART_LINE_THRESHOLD = 0.50
INTENSITY_LINE_THRESHOLD = 0.10
ULTRA_SOUND_THRESHOLD = 12  # cm

# Parameters for the line following
LINE_FOLLOWING_BASE_SPEED = 0.125  # m/s
LINE_FOLLOWING_PID_KP = 0.1
LINE_FOLLOWING_PID_KI = 0.0
LINE_FOLLOWING_PID_KD = 0.0
LINE_FOLLOWING_TURN_SPEED_GAIN = 0.7
LINE_FOLLOWING_SHARP_TURN_SPEED = 0.13  # m/s
LINE_END_DIST = 0.1  # m
LINE_GAP_DIST = 0.04  # m
LINE_END_THRESHOLD = LINE_END_DIST / LINE_FOLLOWING_BASE_SPEED  # s
LINE_GAP_THRESHOLD = LINE_GAP_DIST / LINE_FOLLOWING_BASE_SPEED  # s
TURN_ANGLE_THRESHOLD = deg_to_rad(110)

# Parameters for the return to line
RETURN_TO_LINE_BASE_SPEED = 0.1  # m/s
RETURN_TO_LINE_TURN_SPEED = 0.1  # m/s

# Parameters for the can detection
CAN_DETECTION_BASE_SPEED = 0.02  # m/s
CAN_DECTECTION_SCAN_DEGREES = deg_to_rad(40)

# Parameters for the can pickup
CAN_PICKUP_BASE_SPEED = 0.04  # m/s
CAN_PICKUP_GRIP_SPEED = 0.005  # m/s
CAN_PICKUP_DISTANCE_THRESHOLD = 25  # cm
CAN_PICKUP_MAX_DISTANCE = 6


# Blackboard keys
LAST_TIME_LINE_SEEN = "last_time_line_seen"
CAN_PICKED_UP = "can_picked_up"
RETURNED_TO_LINE = "returned_to_line"
CAN_ANGLE = "can_angle"
POINTING_AT_CAN = "pointing_at_can"


def setup_blackboard() -> BlackBoard:
    blackboard = BlackBoard()
    blackboard[LAST_TIME_LINE_SEEN] = time.time()
    blackboard[CAN_PICKED_UP] = False
    blackboard[RETURNED_TO_LINE] = False
    blackboard[CAN_ANGLE] = None
    blackboard[POINTING_AT_CAN] = False

    return blackboard
