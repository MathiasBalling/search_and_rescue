from actuators import ActuatorsProposal, StopCommand, WheelCommand
from ai.behaviors.behavior import Behavior
from params import (
    CAN_PICKED_UP,
    CAN_ANGLE,
    INTENSITY_PART_LINE_THRESHOLD,
    RETURN_TO_LINE_BASE_SPEED,
    RETURN_TO_LINE_TURN_SPEED,
    RETURNED_TO_LINE,
    deg_to_rad,
)
from sensors.colors import ColorSensors
from sensors.pose import PoseSensor
from utils.blackboard import BlackBoard

TURN_LEFT = WheelCommand(-RETURN_TO_LINE_TURN_SPEED, RETURN_TO_LINE_TURN_SPEED)
TURN_RIGHT = WheelCommand(RETURN_TO_LINE_TURN_SPEED, -RETURN_TO_LINE_TURN_SPEED)


class LineReturnBehavior(Behavior):
    def __init__(
        self,
        blackboard: BlackBoard,
        color_sensors: ColorSensors,
        pose: PoseSensor,
    ):
        super().__init__(blackboard, 0.0)
        self.color_sensors = color_sensors
        self.pose = pose

        self.turn_angle_start = None
        self.target_angle = None

    def update(self):
        self.weight = 0.0
        if self.blackboard[RETURNED_TO_LINE]:
            return

        if not self.blackboard[CAN_PICKED_UP]:
            return
        else:
            self.weight += 5.0

    def actuators_proposal(self):
        left_value, middle_value, right_value = self.color_sensors.get_value()
        if (
            left_value < INTENSITY_PART_LINE_THRESHOLD
            or right_value < INTENSITY_PART_LINE_THRESHOLD
        ):
            self.blackboard[RETURNED_TO_LINE] = True
            # print("Returned to line")
            return ActuatorsProposal(StopCommand())

        x, y, angle = self.pose.get_value()

        if self.turn_angle_start is None:
            self.turn_angle_start = angle

        if self.target_angle is None:
            can_angle = self.blackboard[CAN_ANGLE]
            if can_angle > 0:
                self.target_angle = deg_to_rad(-180) + can_angle
            else:
                self.target_angle = deg_to_rad(180) + can_angle

        if abs(self.target_angle - angle) < deg_to_rad(3):
            return ActuatorsProposal(
                WheelCommand(RETURN_TO_LINE_BASE_SPEED, RETURN_TO_LINE_BASE_SPEED)
            )
        elif self.target_angle - angle < 0:
            return ActuatorsProposal(TURN_LEFT)
        else:
            return ActuatorsProposal(TURN_RIGHT)
