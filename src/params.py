# General parameters
import time
from utils.blackboard import BlackBoard
import math


def dps_to_mps(dps):
    return dps * math.pi / 180.0 * WHEEL_RADIUS


def mps_to_dps(mps):
    dps = mps * 180.0 / math.pi / WHEEL_RADIUS
    return round(max(-MAX_DEGREES_PER_SEC, min(dps, MAX_DEGREES_PER_SEC)))


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
INTENSITY_PART_LINE_THRESHOLD = 0.75
INTENSITY_LINE_THRESHOLD = 0.10


# Parameters for the line following
LINE_FOLLOWING_BASE_SPEED = 0.19  # m/s
LINE_FOLLOWING_PID_KP = 0.13
LINE_FOLLOWING_PID_KI = 0.00
LINE_FOLLOWING_PID_KD = 0.003
LINE_FOLLOWING_TURN_SPEED_GAIN = 0.5
LINE_FOLLOWING_SHARP_TURN_SPEED = 0.13  # m/s
LINE_END_THRESHOLD = 1.0  # s
LINE_GAP_THRESHOLD = 0.5  # s
TURN_ANGLE_THRESHOLD = math.pi / 2  # 90 degrees

# Parameters for the return to line
RETURN_TO_LINE_BASE_SPEED = 0.19  # m/s

# Parameters for the can detection
CAN_DETECTION_BASE_SPEED = 0.2  # m/s
CAN_DETECTION_DISTANCE_THRESHOLD = 20  # cm
CAN_DECTECTION_SCAN_DEGREES = 30

# Parameters for the can pickup
CAN_PICKUP_BASE_SPEED = 0.05  # m/s
CAN_PICKUP_MAX_DISTANCE = 6


# Blackboard keys
LAST_TIME_LINE_SEEN = "last_time_line_seen"
CAN_PICKED_UP = "can_picked_up"
RETURNED_TO_LINE = "returned_to_line"
CAN_SIDE_PICKUP = "can_side_pickup"


def setup_blackboard() -> BlackBoard:
    blackboard = BlackBoard()
    blackboard[LAST_TIME_LINE_SEEN] = time.time()
    blackboard[CAN_PICKED_UP] = False
    blackboard[RETURNED_TO_LINE] = False
    blackboard[CAN_SIDE_PICKUP] = (0, True)

    return blackboard
