# General parameters
import time
from utils.blackboard import BlackBoard
import math


DT = 0.02

MOTOR_OFF = 0
GRIPPER_SPEED = 100

# Robot parameters
WHEEL_RADIUS = 0.0275
WHEEL_CIRCUMFERENCE = WHEEL_RADIUS * 2 * math.pi
WHEEL_SEPARATION = 0.125

INTENSITY_FLOOR_THRESHOLD = 0.9
INTENSITY_PART_LINE_THRESHOLD = 0.75
INTENSITY_LINE_THRESHOLD = 0.10
TURN_TIME_PER_DEGREE = 0.011


# Parameters for the line following
LINE_FOLLOWING_BASE_SPEED = 50
LINE_FOLLOWING_PID_KP = 45.0
LINE_FOLLOWING_PID_KI = 0.0
LINE_FOLLOWING_PID_KD = 1.0
LINE_FOLLOWING_TURN_SPEED_GAIN = 0.5
LINE_FOLLOWING_SHARP_TURN_SPEED = 30
LINE_FOLLOWING_SHARP_TURN_SPEED_BACK = -30
LINE_END_THRESHOLD = 1.0
LINE_GAP_THRESHOLD = 0.5
TURN_ANGLE_THRESHOLD = math.pi / 2  # 90 degrees

# Parameters for the return to line
RETURN_TO_LINE_BASE_SPEED = 50

# Parameters for the can detection
CAN_DETECTION_BASE_SPEED = 40
CAN_DETECTION_DISTANCE_THRESHOLD = 20
CAN_DECTECTION_SCAN_DEGREES = 30

# Parameters for the can pickup
CAN_PICKUP_BASE_SPEED = 20
CAN_PICKUP_MAX_DISTANCE = 6

# Parameters for ramps

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
