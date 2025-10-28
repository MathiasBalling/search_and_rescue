import time
from blackboard import BlackBoard

# General parameters
MOTOR_OFF = 0
BASE_SPEED = 50
LINE_INTENSITY_THRESHOLD = 20
TURN_TIME_PER_DEGREE = 0.01111


# Parameters for the line following
LINE_FOLLOWING_BASE_SPEED = 50
LINE_FOLLOWING_PID_KP = 2.5
LINE_FOLLOWING_PID_KI = 0.0
LINE_FOLLOWING_PID_KD = 1.0

# Parameters for the return to line
RETURN_TO_LINE_BASE_SPEED = 50

# Parameters for the can detection
CAN_DETECTION_BASE_SPEED = 20
CAN_DETECTION_DISTANCE_THRESHOLD = 20

# Parameters for the can pickup
CAN_PICKUP_BASE_SPEED = 15

# Parameters for ramps
RAMP_DETECTION_DISTANCE_THRESHOLD = 20
RAMP_DETECTION_SPEED = 30


def setup_blackboard(blackboard: BlackBoard):
    blackboard["can_picked_up"] = False
    blackboard["on_line"] = False
    blackboard["returned_to_line"] = False
    blackboard["last_time_line_seen"] = time.time()
