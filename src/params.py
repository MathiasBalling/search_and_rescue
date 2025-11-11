# General parameters
import time
from utils.blackboard import BlackBoard


DT = 0.01

MOTOR_OFF = 0
GRIPPER_SPEED = 100

LINE_INTENSITY_WHITE_THRESHOLD = 25
LINE_INTENSITY_BLACK_THRESHOLD = 6
TURN_TIME_PER_DEGREE = 0.01111


# Parameters for the line following
LINE_FOLLOWING_BASE_SPEED = 40
LINE_FOLLOWING_PID_KP = 2.5
LINE_FOLLOWING_PID_KI = 0.0
LINE_FOLLOWING_PID_KD = 0.0
LINE_FOLLOWING_SHARP_TURN_SPEED = 100
LINE_FOLLOWING_SHARP_TURN_SPEED_BACK = -20

# Parameters for the return to line
RETURN_TO_LINE_BASE_SPEED = 50

# Parameters for the can detection
CAN_DETECTION_BASE_SPEED = 20
CAN_DETECTION_DISTANCE_THRESHOLD = 20

# Parameters for the can pickup
CAN_PICKUP_BASE_SPEED = 20
CAN_PICKUP_MAX_DISTANCE = 6

# Parameters for ramps


# Blackboard keys
LAST_TIME_LINE_SEEN = "last_time_line_seen"
CAN_PICKED_UP = "can_picked_up"
RETURNED_TO_LINE = "returned_to_line"


def setup_blackboard() -> BlackBoard:
    blackboard = BlackBoard()
    blackboard[LAST_TIME_LINE_SEEN] = time.time()
    blackboard[CAN_PICKED_UP] = False
    blackboard[RETURNED_TO_LINE] = False

    return blackboard
