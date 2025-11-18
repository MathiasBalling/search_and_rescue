from actuators import ActuatorsProposal, TurnCommand, WheelCommand
from ai.behaviors.behavior import Behavior
from params import CAN_PICKED_UP, RETURN_TO_LINE_BASE_SPEED, RETURNED_TO_LINE
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
            # TODO: Maybe keep track of where the can was relative to the line for a more accurate turn around
            return ActuatorsProposal(TurnCommand(180, True))

        # We did turn around after finding the can, now use search until we find the line
        # TODO: Maybe use the ultrasonic sensor to aboid colisions until the line is found.

        
        return WheelCommand(RETURN_TO_LINE_BASE_SPEED, RETURN_TO_LINE_BASE_SPEED)

