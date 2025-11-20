from actuators import ActuatorsProposal, TurnCommand, WheelCommand
from ai.behaviors.behavior import Behavior
from params import (
    CAN_PICKED_UP,
    CAN_SIDE_PICKUP,
    LINE_INTENSITY_BLACK_THRESHOLD,
    LINE_INTENSITY_WHITE_THRESHOLD,
    RETURN_TO_LINE_BASE_SPEED,
    RETURNED_TO_LINE,
)
from sensors.colors import ColorSensors
from utils.blackboard import BlackBoard


class LineReturnBehavior(Behavior):
    def __init__(
        self,
        blackboard: BlackBoard,
        color_sensors: ColorSensors,
    ):
        super().__init__(blackboard, 0.0)
        self.color_sensors = color_sensors
        self.did_turn = False

    def update(self):
        self.weight = 0.5
        if self.blackboard[RETURNED_TO_LINE]:
            self.weight = 0.0
            return

        if not self.blackboard[CAN_PICKED_UP]:
            self.weight = 0.0
            return
        else:
            self.weight += 5.0

    def actuators_proposal(self):
        if not self.did_turn:
            self.did_turn = True

            can_degree, ccw = self.blackboard[CAN_SIDE_PICKUP]
            if ccw:
                if can_degree > 0:
                    return ActuatorsProposal(TurnCommand(180 + can_degree, True))
                else:
                    return ActuatorsProposal(TurnCommand(180 + can_degree, False))
            else:
                if can_degree > 0:
                    return ActuatorsProposal(TurnCommand(180 + can_degree, False))
                else:
                    return ActuatorsProposal(TurnCommand(180 + can_degree, True))

        # We did turn around after finding the can, now use search until we find the line
        # TODO: Maybe keep track of where the can was relative to the line for a more accurate turn around
        left_value, right_value = self.color_sensors.get_value()
        if (
            left_value < LINE_INTENSITY_BLACK_THRESHOLD
            or right_value < LINE_INTENSITY_BLACK_THRESHOLD
        ):
            self.blackboard[RETURNED_TO_LINE] = True
            return ActuatorsProposal(WheelCommand(0, 0))

        return ActuatorsProposal(
            WheelCommand(RETURN_TO_LINE_BASE_SPEED, RETURN_TO_LINE_BASE_SPEED)
        )
